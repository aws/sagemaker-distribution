import argparse
import base64
import copy
import glob
import os
import shutil

import boto3
import docker
import pytest
from conda.models.match_spec import MatchSpec
from docker.errors import BuildError, ContainerError
from semver import Version

from changelog_generator import generate_change_log
from config import _image_generator_configs
from dependency_upgrader import (
    _MAJOR,
    _MINOR,
    _PATCH,
    _get_dependency_upper_bound_for_runtime_upgrade,
)
from package_staleness import generate_package_staleness_report
from release_notes_generator import generate_release_notes
from utils import (
    get_dir_for_version,
    get_match_specs,
    get_semver,
    is_exists_dir_for_version,
)

_docker_client = docker.from_env()


def create_and_get_semver_dir(version: Version, exist_ok: bool = False):
    dir = get_dir_for_version(version)

    if os.path.exists(dir):
        if not exist_ok:
            raise Exception()
        if not os.path.isdir(dir):
            raise Exception()
        # Delete all files except the additional_packages_env_in_file
        _delete_all_files_except_additional_packages_input_files(dir)
    else:
        os.makedirs(dir)
    return dir


def _delete_all_files_except_additional_packages_input_files(base_version_dir):
    additional_package_env_in_files = [
        image_generator_config["additional_packages_env_in_file"] for image_generator_config in _image_generator_configs
    ]
    for filename in os.listdir(base_version_dir):
        if filename not in additional_package_env_in_files:
            file_path = os.path.join(base_version_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))


def _create_new_version_artifacts(args):
    runtime_version_upgrade_type = args.runtime_version_upgrade_type

    if runtime_version_upgrade_type == _PATCH:
        runtime_version_upgrade_func = "bump_patch"
    elif runtime_version_upgrade_type == _MINOR:
        runtime_version_upgrade_func = "bump_minor"
    elif runtime_version_upgrade_type == _MAJOR:
        runtime_version_upgrade_func = "bump_major"
    else:
        raise Exception()

    base_patch_version = get_semver(args.base_patch_version)
    if base_patch_version.prerelease:
        # We don't support creating new patch/major/minor versions from a prerelease version
        # Re-run the build command for the prerelease version again to pick the latest versions
        # of the marquee packages
        raise Exception()
    next_version = getattr(base_patch_version, runtime_version_upgrade_func)()

    if args.pre_release_identifier:
        next_version = next_version.replace(prerelease=args.pre_release_identifier)

    base_version_dir = get_dir_for_version(base_patch_version)
    new_version_dir = create_and_get_semver_dir(next_version, args.force)

    for image_generator_config in _image_generator_configs:
        _create_new_version_conda_specs(
            base_version_dir, new_version_dir, runtime_version_upgrade_type, image_generator_config
        )

    _copy_static_files(base_version_dir, new_version_dir, str(next_version.major), runtime_version_upgrade_type)
    with open(f"{new_version_dir}/source-version.txt", "w") as f:
        f.write(args.base_patch_version)


def _copy_static_files(base_version_dir, new_version_dir, new_version_major, runtime_version_upgrade_type):
    for f in glob.glob(f"{base_version_dir}/gpu.arg_based_env.in"):
        shutil.copy2(f, new_version_dir)
    for f in glob.glob(f"{base_version_dir}/patch_*"):
        shutil.copy2(f, new_version_dir)

    # For patches, get Dockerfile+dirs from base patch
    # For minor/major, get Dockerfile+dirs from template
    if runtime_version_upgrade_type == _PATCH:
        base_path = base_version_dir
    else:
        base_path = f"template/v{new_version_major}"
    for f in glob.glob(os.path.relpath(f"{base_path}/Dockerfile")):
        shutil.copy2(f, new_version_dir)
    if int(new_version_major) >= 1:
        # dirs directory doesn't exist for v0. It was introduced only for v1
        dirs_relative_path = os.path.relpath(f"{base_path}/dirs")
        for f in glob.glob(dirs_relative_path):
            shutil.copytree(f, os.path.join(new_version_dir, "dirs"))


def _create_new_version_conda_specs(
    base_version_dir, new_version_dir, runtime_version_upgrade_type, image_generator_config
):
    env_in_filename = image_generator_config["build_args"]["ENV_IN_FILENAME"]
    additional_packages_env_in_filename = image_generator_config["additional_packages_env_in_file"]
    env_out_filename = image_generator_config["env_out_filename"]

    base_match_specs_in = get_match_specs(f"{base_version_dir}/{env_in_filename}")

    base_match_specs_out = get_match_specs(f"{base_version_dir}/{env_out_filename}")
    additional_packages_match_specs_in = get_match_specs(f"{new_version_dir}/{additional_packages_env_in_filename}")

    # Add all the match specs from the previous version.
    # If a package is present in both additional packages as well as the previous version, then
    # use the values in the previous version
    additional_packages_match_specs_in.update(base_match_specs_in)

    out = []
    for package_name in additional_packages_match_specs_in:
        match_out: MatchSpec = base_match_specs_out.get(package_name)

        if match_out is None:
            # No restriction on what versions to use.
            out.append(f"conda-forge::{package_name}")
        else:
            channel = match_out.get("channel").channel_name

            min_version_inclusive = match_out.get("version")
            assert str(min_version_inclusive).startswith("==")
            min_version_inclusive = str(min_version_inclusive).removeprefix("==")

            max_version_str = _get_dependency_upper_bound_for_runtime_upgrade(
                package_name, min_version_inclusive, runtime_version_upgrade_type
            )

            out.append(f"{channel}::{package_name}[version='>={min_version_inclusive}{max_version_str}']")

    with open(f"{new_version_dir}/{env_in_filename}", "w") as f:
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
    image_ids, image_versions = _build_local_images(target_version, args.target_ecr_repo, args.force, args.skip_tests)
    generate_release_notes(target_version)

    # Upload to ECR before running tests so that only the exact image which we tested goes to public
    # TODO: Move after tests are stabilized
    if args.target_ecr_repo is not None:
        _push_images_upstream(image_versions, args.region)

    if not args.skip_tests:
        print(f"Will now run tests against: {image_ids}")
        _test_local_images(image_ids, args.target_patch_version)
    else:
        print("Will skip tests.")


def _push_images_upstream(image_versions_to_push: list[dict[str, str]], region: str):
    print(f"Will now push the images to ECR: {image_versions_to_push}")

    for i in image_versions_to_push:
        username, password = _get_ecr_credentials(region, i["repository"])
        _docker_client.images.push(
            repository=i["repository"], tag=i["tag"], auth_config={"username": username, "password": password}
        )

    print(f"Successfully pushed these images to ECR: {image_versions_to_push}")


def _test_local_images(image_ids_to_test: list[str], target_version: str):
    assert len(image_ids_to_test) == len(_image_generator_configs)
    exit_codes = []
    image_ids = []
    for image_id, config in zip(image_ids_to_test, _image_generator_configs):
        exit_code = pytest.main(
            ["-n", "2", "-m", config["image_type"], "--local-image-version", target_version, *config["pytest_flags"]]
        )

        assert exit_code == 0, f"Tests failed with exit codes: {exit_codes} against: {image_ids}"

    print(f"Tests ran successfully against: {image_ids_to_test}")


def _get_config_for_image(target_version_dir: str, image_generator_config, force_rebuild) -> dict:
    if not os.path.exists(target_version_dir + "/" + image_generator_config["env_out_filename"]) or force_rebuild:
        return image_generator_config

    config_for_image = copy.deepcopy(image_generator_config)
    # Use the existing env.out to create the conda environment. Pass that as env.in
    config_for_image["build_args"]["ENV_IN_FILENAME"] = image_generator_config["env_out_filename"]
    # Remove ARG_BASED_ENV_IN_FILENAME if it exists
    config_for_image["build_args"].pop("ARG_BASED_ENV_IN_FILENAME", None)
    return config_for_image


# Returns a tuple of: 1/ list of actual images generated; 2/ list of tagged images. A given image can be tagged by
# multiple different strings - for e.g., a CPU image can be tagged as '1.3.2-cpu', '1.3-cpu', '1-cpu' and/or
# 'latest-cpu'. Therefore, (1) is strictly a subset of (2).
def _build_local_images(
    target_version: Version, target_ecr_repo_list: list[str], force: bool, skip_tests=False
) -> (list[str], list[dict[str, str]]):
    target_version_dir = get_dir_for_version(target_version)

    generated_image_ids = []
    generated_image_versions = []

    for image_generator_config in _image_generator_configs:
        config = _get_config_for_image(target_version_dir, image_generator_config, force)
        try:
            image, log_gen = _docker_client.images.build(
                path=target_version_dir, rm=True, pull=True, buildargs=config["build_args"]
            )
        except BuildError as e:
            for line in e.build_log:
                if "stream" in line:
                    print(line["stream"].strip())
            # After printing the logs, raise the exception (which is the old behavior)
            raise
        print(f"Successfully built an image with id: {image.id}")
        generated_image_ids.append(image.id)
        try:
            container_logs = _docker_client.containers.run(
                image=image.id, detach=False, auto_remove=True, command="micromamba env export --explicit"
            )
        except ContainerError as e:
            print(e.container.logs().decode("utf-8"))
            # After printing the logs, raise the exception (which is the old behavior)
            raise

        with open(f'{target_version_dir}/{config["env_out_filename"]}', "wb") as f:
            f.write(container_logs)

        # Generate change logs. Use the original image generator config which contains the name
        # of the actual env.in file instead of the 'config'.
        generate_change_log(target_version, image_generator_config)

        version_tags_to_apply = _get_version_tags(target_version, config["env_out_filename"])
        image_tags_to_apply = [config["image_tag_generator"].format(image_version=i) for i in version_tags_to_apply]

        if target_ecr_repo_list is not None:
            for target_ecr_repo in target_ecr_repo_list:
                for t in image_tags_to_apply:
                    image.tag(target_ecr_repo, tag=t)
                    generated_image_versions.append({"repository": target_ecr_repo, "tag": t})

        # Tag the image for testing
        image.tag(
            "localhost/sagemaker-distribution", config["image_tag_generator"].format(image_version=str(target_version))
        )

    return generated_image_ids, generated_image_versions


# At some point of time, let's say some patch versions exist for both 2.6 and 2.7, and we create new patch
# versions for both of them. Now, for the new 2.6.x, we can tag it as '2.6.x-cpu' and '2.6-cpu' but NOT '2-cpu' because
# there is a more recent version (i.e. 2.7.x) that should be considered '2-cpu'. So, given a patch version, the
# following function returns a list of versions for which the current patch version is latest for.
def _get_version_tags(target_version: Version, env_out_file_name: str) -> list[str]:
    # First, add '2.6.x' as is.
    res = [str(target_version)]
    # If this is a pre-release version, then don't add additional tags
    if target_version.prerelease:
        return res

    # If we were to add '2.6', check if '2.6.(x+1)' is present.
    if not is_exists_dir_for_version(target_version.bump_patch(), env_out_file_name):
        res.append(f"{target_version.major}.{target_version.minor}")
    else:
        return res

    # If we were to add '2', check if '2.7' is present.
    if not is_exists_dir_for_version(target_version.bump_minor(), env_out_file_name):
        res.append(str(target_version.major))
    else:
        return res

    # If we were to add 'latest', check if '3.0.0' is present.
    if not is_exists_dir_for_version(target_version.bump_major(), env_out_file_name):
        res.append("latest")

    return res


def _get_ecr_credentials(region, repository: str) -> (str, str):
    _ecr_client_config_name = "ecr-public" if repository.startswith("public.ecr.aws") else "ecr"
    _ecr_client = boto3.client(_ecr_client_config_name, region_name=region)
    _authorization_data = _ecr_client.get_authorization_token()["authorizationData"]
    if _ecr_client_config_name == "ecr":
        # If we are using the ecr private client, then fetch the first index from authorizationData
        _authorization_data = _authorization_data[0]
    return base64.b64decode(_authorization_data["authorizationToken"]).decode().split(":")


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="A command line utility to create new versions of Amazon SageMaker Distribution"
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    create_major_version_parser = subparsers.add_parser(
        "create-major-version-artifacts", help="Creates a new major version of Amazon SageMaker Distribution."
    )
    create_major_version_parser.set_defaults(func=create_major_version_artifacts, runtime_version_upgrade_type=_MAJOR)

    create_minor_version_parser = subparsers.add_parser(
        "create-minor-version-artifacts", help="Creates a new minor version of Amazon SageMaker Distribution."
    )
    create_minor_version_parser.set_defaults(func=create_minor_version_artifacts, runtime_version_upgrade_type=_MINOR)

    create_patch_version_parser = subparsers.add_parser(
        "create-patch-version-artifacts", help="Creates a new patch version of Amazon SageMaker Distribution."
    )
    create_patch_version_parser.set_defaults(func=create_patch_version_artifacts, runtime_version_upgrade_type=_PATCH)

    # Common arguments
    for p in [create_major_version_parser, create_minor_version_parser, create_patch_version_parser]:
        p.add_argument(
            "--base-patch-version",
            required=True,
            help="Specify the base patch version from which a new version should be created.",
        )
        p.add_argument(
            "--pre-release-identifier",
            help="Optionally specify the pre-release identifier for this new version that should " "be created.",
        )
        p.add_argument(
            "--force",
            action="store_true",
            help="Overwrites any existing directory corresponding to the new version that will be generated.",
        )

    build_image_parser = subparsers.add_parser("build", help="Builds a new image from the Dockerfile.")
    build_image_parser.add_argument(
        "--target-patch-version",
        required=True,
        help="Specify the target version of Amazon SageMaker Distribution for which an image needs to be built.",
    )
    build_image_parser.add_argument(
        "--skip-tests", action="store_true", help="Disable running tests against the newly generated Docker image."
    )
    build_image_parser.add_argument(
        "--force",
        action="store_true",
        help="Builds a new docker image which will fetch the latest versions of each package in "
        "the conda environment. Any existing env.out file will be overwritten.",
    )
    build_image_parser.add_argument(
        "--target-ecr-repo",
        action="append",
        help="Specify the AWS ECR repository in which this image needs to be uploaded.",
    )
    build_image_parser.add_argument("--region", help="Specify the region of the ECR repository.")
    build_image_parser.set_defaults(func=build_images)
    package_staleness_parser = subparsers.add_parser(
        "generate-staleness-report",
        help="Generates package staleness report for each of the marquee packages in the given " "image version.",
    )
    package_staleness_parser.set_defaults(func=generate_package_staleness_report)
    package_staleness_parser.add_argument(
        "--target-patch-version",
        required=True,
        help="Specify the base patch version for which the package staleness report needs to be " "generated.",
    )
    return parser


def parse_args(parser):
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    parse_args(get_arg_parser())
