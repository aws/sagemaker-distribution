import conda.cli.python_api
import json
from utils import (
    get_dir_for_version,
    get_semver,
    get_match_specs,
)
from config import _image_generator_configs
from dependency_upgrader import _dependency_metadata
from conda.models.match_spec import MatchSpec


def _get_package_versions_in_upstream(target_packages_match_spec_out, target_version) \
        -> dict[str, str]:
    package_to_version_mapping = {}
    is_major_version_release = target_version.minor == 0 and target_version.patch == 0
    is_minor_version_release = target_version.patch == 0 and not is_major_version_release
    for package in target_packages_match_spec_out:
        # Execute a conda search api call in the linux-64 subdirectory
        # packages such as pytorch-gpu are present only in linux-64 sub directory
        match_spec_out = target_packages_match_spec_out[package]
        package_version = str(match_spec_out.get("version")).removeprefix('==')
        package_version = get_semver(package_version)
        channel = match_spec_out.get("channel").channel_name
        subdir_filter = '[subdir=' + match_spec_out.get('subdir') + ']'
        search_result = conda.cli.python_api.run_command('search', channel + '::' + package +
                                                         '>=' + str(package_version) +
                                                         subdir_filter, '--json')
        # Load the first result as json. The API sends a json string inside an array
        package_metadata = json.loads(search_result[0])[package]
        # Response is of the structure
        # { 'package_name': [{'url':<someurl>, 'dependencies': <List of dependencies>, 'version':
        # <version number>}, ..., {'url':<someurl>, 'dependencies': <List of dependencies>, 'version':
        # <version number>}]
        # We only care about the version number in the last index
        package_version_in_conda = ''
        if is_major_version_release:
            latest_package_version_in_conda = package_metadata[-1]['version']
        elif is_minor_version_release:
            package_major_version_prefix = str(package_version.major) + "."
            latest_package_version_in_conda = [x['version'] for x in package_metadata if
                                        x['version'].startswith(package_major_version_prefix)][-1]
        else:
            package_minor_version_prefix = \
                ".".join([str(package_version.major), str(package_version.minor)]) + "."
            latest_package_version_in_conda = [x['version'] for x in package_metadata if
                                        x['version'].startswith(package_minor_version_prefix)][-1]

        package_to_version_mapping[package] = latest_package_version_in_conda
    return package_to_version_mapping


def _generate_report(package_versions_in_upstream, target_packages_match_spec_out, image_config,
                     version):
    print('\n# Staleness Report: ' + str(version) + '(' + image_config['image_type'] + ')\n')
    print('Package | Current Version in the Distribution image | Latest Relevant Version in '
          'Upstream')
    print('---|---|---')
    for package in package_versions_in_upstream:
        version_in_sagemaker_distribution = \
            str(target_packages_match_spec_out[package].get('version')).removeprefix('==')
        if version_in_sagemaker_distribution == package_versions_in_upstream[package]:
            print(package + '|' + version_in_sagemaker_distribution + '|' +
                  package_versions_in_upstream[package])
        else:
            print('${\color{red}' + package + '}$' + '|' + version_in_sagemaker_distribution +
                  '|' + package_versions_in_upstream[package])


def _get_installed_package_versions_and_conda_versions(image_config, target_version_dir,
                                                       target_version) \
        -> (dict[str, MatchSpec], dict[str, str]):
    env_in_file_name = image_config['build_args']['ENV_IN_FILENAME']
    env_out_file_name = image_config['env_out_filename']
    required_packages_from_target = get_match_specs(
        target_version_dir + "/" + env_in_file_name
    ).keys()
    match_spec_out = get_match_specs(target_version_dir + "/" + env_out_file_name)
    # We only care about packages which are present in env.in
    # Remove Python from the dictionary, we don't want to track python version as part of our
    # staleness report.
    target_packages_match_spec_out = {k: v for k, v in match_spec_out.items()
                                      if k in required_packages_from_target and k
                                      not in _dependency_metadata}
    latest_package_versions_in_upstream = \
        _get_package_versions_in_upstream(target_packages_match_spec_out,
                                             target_version)
    return target_packages_match_spec_out, latest_package_versions_in_upstream


def generate_package_staleness_report(args):
    target_version = get_semver(args.target_patch_version)
    target_version_dir = get_dir_for_version(target_version)
    for image_config in _image_generator_configs:
        target_packages_match_spec_out, latest_package_versions_in_upstream = \
            _get_installed_package_versions_and_conda_versions(image_config, target_version_dir,
                                                               target_version)
        _generate_report(latest_package_versions_in_upstream, target_packages_match_spec_out,
                         image_config, target_version)
