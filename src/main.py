import argparse
import base64
import glob
import os
import shutil
from typing import List

import boto3
import docker
import pytest
from conda.models.match_spec import MatchSpec
from conda_env.specs import RequirementsSpec
from semver import Version

from dependency_upgrader import _get_dependency_upper_bound_for_runtime_upgrade, _MAJOR, _MINOR, _PATCH
from config import _image_generator_configs

_docker_client = docker.from_env()


def get_semver(version_str) -> Version:
    version = Version.parse(version_str)
    if version.prerelease is not None or version.build is not None:
        raise Exception()
    return version


def is_exists_dir_for_version(version: Version) -> bool:
    dir_path = get_dir_for_version(version)
    return os.path.exists(dir_path)


def get_dir_for_version(version: Version) -> str:
    return os.path.relpath(f'build_artifacts/v{version.major}/v{version.major}.{version.minor}/'
                           f'v{version.major}.{version.minor}.{version.patch}')


def create_and_get_semver_dir(version: Version, exist_ok: bool = False):
    dir = get_dir_for_version(version)

    if os.path.exists(dir):
        if not exist_ok:
            raise Exception()
        if not os.path.isdir(dir):
            raise Exception()
        shutil.rmtree(dir)

    os.makedirs(dir)
    return dir


def read_env_file(file_path) -> RequirementsSpec:
    return RequirementsSpec(filename=file_path)


def get_match_specs(file_path) -> List[MatchSpec]:
    if not os.path.isfile(file_path):
        return []

    requirement_spec = read_env_file(file_path)
    assert len(requirement_spec.environment.dependencies) == 1
    assert 'conda' in requirement_spec.environment.dependencies

    return [MatchSpec(i) for i in requirement_spec.environment.dependencies['conda']]


def _create_new_version_artifacts(args):
    runtime_version_upgrade_type = args.runtime_version_upgrade_type

    if runtime_version_upgrade_type == _PATCH:
        runtime_version_upgrade_func = 'bump_patch'
    elif runtime_version_upgrade_type == _MINOR:
        runtime_version_upgrade_func = 'bump_minor'
    elif runtime_version_upgrade_type == _MAJOR:
        runtime_version_upgrade_func = 'bump_major'
    else:
        raise Exception()

    base_patch_version = get_semver(args.base_patch_version)
    next_version = getattr(base_patch_version, runtime_version_upgrade_func)()

    base_version_dir = get_dir_for_version(base_patch_version)
    new_version_dir = create_and_get_semver_dir(next_version, args.force)

    for image_generator_config in _image_generator_configs:
        _create_new_version_conda_specs(base_version_dir, new_version_dir, runtime_version_upgrade_type,
                                        image_generator_config)

    _copy_static_files(base_version_dir, new_version_dir)


def _copy_static_files(base_version_dir, new_version_dir):
    for name in ['gpu.arg_based_env.in', 'Dockerfile']:
        for f in glob.glob(f'{base_version_dir}/{name}'):
            shutil.copy2(f, new_version_dir)


def _create_new_version_conda_specs(base_version_dir, new_version_dir, runtime_version_upgrade_type,
                                    image_generator_config):
    env_in_filename = image_generator_config['build_args']['ENV_IN_FILENAME']
    env_out_filename = image_generator_config['env_out_filename']

    base_match_specs_in = get_match_specs(f'{base_version_dir}/{env_in_filename}')

    base_match_specs_out = get_match_specs(f'{base_version_dir}/{env_out_filename}')
    base_match_specs_out_dict = {m.get('name'): m for m in base_match_specs_out}

    out = []
    for match_in in base_match_specs_in:
        package_name = match_in.get("name")
        match_out: MatchSpec = base_match_specs_out_dict.get(match_in.get('name'))

        if match_out is None:
            # No restriction on what versions to use.
            out.append(f"conda-forge::{package_name}")
        else:
            channel = match_out.get("channel").channel_name

            min_version_inclusive = match_out.get('version')
            assert str(min_version_inclusive).startswith('==')
            min_version_inclusive = str(min_version_inclusive).removeprefix('==')

            max_version_str = _get_dependency_upper_bound_for_runtime_upgrade(package_name,
                                                                              min_version_inclusive,
                                                                              runtime_version_upgrade_type)

            out.append(f"{channel}::{package_name}[version='>={min_version_inclusive},{max_version_str}']")

    with open(f'{new_version_dir}/{env_in_filename}', 'w') as f:
        f.write("# This file is auto-generated.\n")
        f.write("\n".join(out))
        f.write("\n")  # This new line is pretty important. See code documentation in Dockerfile for the reasoning.


def create_major_version_artifacts(args):
    _create_new_version_artifacts(args)


def create_minor_version_artifacts(args):
    _create_new_version_artifacts(args)


def create_patch_version_artifacts(args):
    _create_new_version_artifacts(args)


def build_images(args):
    target_version = get_semver(args.target_patch_version)
    image_ids, image_versions = _build_local_images(target_version, args.target_ecr_repo)

    if not args.skip_tests:
        print(f'Will now run tests against: {image_ids}')
        _test_local_images(image_ids)
    else:
        print('Will skip tests.')

    # We only upload to ECR once all images are successfully built locally.
    if args.target_ecr_repo is not None:
        _push_images_upstream(image_versions, args.region)


def _push_images_upstream(image_versions_to_push: list[dict[str, str]], region: str):
    print(f'Will now push the images to ECR: {image_versions_to_push}')

    for i in image_versions_to_push:
        username, password = _get_ecr_credentials(region, i['repository'])
        _docker_client.images.push(repository=i['repository'], tag=i['tag'],
                                   auth_config={'username': username, 'password': password})

    print(f'Successfully pushed these images to ECR: {image_versions_to_push}')


def _test_local_images(image_ids_to_test: list[str]):
    assert len(image_ids_to_test) == len(_image_generator_configs)
    for (image_id, config) in zip(image_ids_to_test, _image_generator_configs):
        exit_code = pytest.main(['-n', '2', '-m', 'slow', '--local-image-id', image_id, *config['pytest_flags']])

        assert exit_code == 0, f'Tests failed with exit code: {exit_code} against: {image_id}'

    print(f'Tests ran successfully against: {image_ids_to_test}')


# Returns a tuple of: 1/ list of actual images generated; 2/ list of tagged images. A given image can be tagged by
# multiple different strings - for e.g., a CPU image can be tagged as '1.3.2-cpu', '1.3-cpu', '1-cpu' and/or
# 'latest-cpu'. Therefore, (1) is strictly a subset of (2).
def _build_local_images(target_version: Version, target_ecr_repo_list: list[str]) -> (list[str], list[dict[str, str]]):
    target_version_dir = get_dir_for_version(target_version)

    generated_image_ids = []
    generated_image_versions = []

    for config in _image_generator_configs:
        image, log_gen = _docker_client.images.build(path=target_version_dir, rm=True, pull=True,
                                                     buildargs=config['build_args'])
        print(f'Successfully built an image with id: {image.id}')
        generated_image_ids.append(image.id)

        container_logs = _docker_client.containers.run(image=image.id, detach=False, auto_remove=True,
                                                       command='micromamba env export --explicit')
        with open(f'{target_version_dir}/{config["env_out_filename"]}', 'wb') as f:
            f.write(container_logs)

        version_tags_to_apply = _get_version_tags(target_version)
        image_tags_to_apply = [config['image_tag_generator'].format(image_version=i) for i in version_tags_to_apply]

        if target_ecr_repo_list is not None:
            for target_ecr_repo in target_ecr_repo_list:
                for t in image_tags_to_apply:
                    image.tag(target_ecr_repo, tag=t)
                    generated_image_versions.append({'repository': target_ecr_repo, 'tag': t})

    return generated_image_ids, generated_image_versions


# At some point of time, let's say some patch versions exist for both 2.6 and 2.7, and we create new patch
# versions for both of them. Now, for the new 2.6.x, we can tag it as '2.6.x-cpu' and '2.6-cpu' but NOT '2-cpu' because
# there is a more recent version (i.e. 2.7.x) that should be considered '2-cpu'. So, given a patch version, the
# following function returns a list of versions for which the current patch version is latest for.
def _get_version_tags(target_version: Version) -> list[str]:
    # First, add '2.6.x' as is.
    res = [str(target_version)]

    # If we were to add '2.6', check if '2.6.(x+1)' is present.
    if not is_exists_dir_for_version(target_version.bump_patch()):
        res.append(f'{target_version.major}.{target_version.minor}')
    else:
        return res

    # If we were to add '2', check if '2.7' is present.
    if not is_exists_dir_for_version(target_version.bump_minor()):
        res.append(str(target_version.major))
    else:
        return res

    # If we were to add 'latest', check if '3.0.0' is present.
    if not is_exists_dir_for_version(target_version.bump_major()):
        res.append('latest')

    return res


def _get_ecr_credentials(region, repository: str) -> (str, str):
    _ecr_client_config_name = 'ecr-public' if repository.startswith('public.ecr.aws') else 'ecr'
    _ecr_client = boto3.client(_ecr_client_config_name, region_name=region)
    _authorization_data = _ecr_client.get_authorization_token()['authorizationData']
    if _ecr_client_config_name == 'ecr':
        # If we are using the ecr private client, then fetch the first index from authorizationData
        _authorization_data = _authorization_data[0]
    return base64.b64decode(_authorization_data['authorizationToken']).decode().split(':')


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="A command line utility to create new versions of Amazon SageMaker Distribution"
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    create_major_version_parser = subparsers.add_parser(
        "create-major-version-artifacts",
        help="Creates a new major version of Amazon SageMaker Distribution."
    )
    create_major_version_parser.set_defaults(func=create_major_version_artifacts,
                                             runtime_version_upgrade_type=_MAJOR)

    create_minor_version_parser = subparsers.add_parser(
        "create-minor-version-artifacts",
        help="Creates a new minor version of Amazon SageMaker Distribution."
    )
    create_minor_version_parser.set_defaults(func=create_minor_version_artifacts,
                                             runtime_version_upgrade_type=_MINOR)

    create_patch_version_parser = subparsers.add_parser(
        "create-patch-version-artifacts",
        help="Creates a new patch version of Amazon SageMaker Distribution."
    )
    create_patch_version_parser.set_defaults(func=create_patch_version_artifacts,
                                             runtime_version_upgrade_type=_PATCH)

    # Common arguments
    for p in [create_major_version_parser, create_minor_version_parser, create_patch_version_parser]:
        p.add_argument(
            "--base-patch-version",
            required=True,
            help="Specify the base patch version from which a new version should be created."
        )
        p.add_argument(
            "--force",
            action='store_true',
            help="Overwrites any existing directory corresponding to the new version that will be generated."
        )

    build_image_parser = subparsers.add_parser(
        "build",
        help="Builds a new image from the Dockerfile."
    )
    build_image_parser.add_argument(
        "--target-patch-version",
        required=True,
        help="Specify the target version of Amazon SageMaker Distribution for which an image needs to be built."
    )
    build_image_parser.add_argument(
        "--skip-tests",
        action='store_true',
        help="Disable running tests against the newly generated Docker image."
    )
    build_image_parser.add_argument(
        "--target-ecr-repo",
        action='append',
        help="Specify the AWS ECR repository in which this image needs to be uploaded."
    )
    build_image_parser.add_argument(
        "--region",
        help="Specify the region of the ECR repository."
    )
    build_image_parser.set_defaults(func=build_images)
    return parser


def parse_args(parser):
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    parse_args(get_arg_parser())
