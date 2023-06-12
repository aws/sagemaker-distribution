import os
import re


def _get_required_packages_from_env_in(file_path) -> set[str]:
    required_packages = set()
    if not os.path.exists(file_path):
        return required_packages
    with open(file_path, 'r') as f:
        lines = f.readlines()
        required_packages = {line.strip().split("::")[1].split("[")[0] for line in lines if line.startswith('conda-forge::')}
    return required_packages


def _get_installed_packages_from_env_out(file_path) -> dict[str, str]:
    installed_packages = dict()
    if not os.path.exists(file_path):
        return installed_packages
    with open(file_path, 'r') as f:
        lines = f.readlines()
        conda_lines = [line for line in lines if line.startswith('https://conda.anaconda.org')]
        for line in conda_lines:
            # re.findall will give the output in the following format
            # [(package_name, version)]. In some cases, the first result returned by this regex
            # can be linux, 64 (if the platform is linux-64). Hence, fetching the last index.
            package_name, version = re.findall(r"/([a-z\.A-Z0-9_-]+)-(\d+[\.\d+]*)", line)[-1]
            installed_packages[package_name] = version
    return installed_packages


def _derive_changeset(target_version_dir, source_version_dir, processor) -> (dict[str, list[str]], dict[str, str]):
    env_in_file_name = processor + '.env.in'
    env_out_file_name = processor + '.env.out'
    required_packages_from_target = _get_required_packages_from_env_in(
        target_version_dir + "/" + env_in_file_name
    )
    # Note: required_packages_from_source is not currently used.
    # In the future, If we remove any packages from env.in, at that time required_packages_from_source will be needed.
    installed_packages_from_target = _get_installed_packages_from_env_out(
        target_version_dir + "/" + env_out_file_name
    )
    installed_packages_from_source = _get_installed_packages_from_env_out(
        source_version_dir + "/" + env_out_file_name
    )
    # We only care about the packages which are present in the target version env.in file
    installed_packages_from_target = {k: v for k, v in installed_packages_from_target.items()
                                      if k in required_packages_from_target}
    # Note: A required package in the target version might not be a required package in the source version
    # But source version could still have this package pulled as a dependency of a dependency.
    installed_packages_from_source = {k: v for k, v in installed_packages_from_source.items()
                                      if k in required_packages_from_target}
    upgrades = {k: [installed_packages_from_source[k], v] for k, v in installed_packages_from_target.items()
                if k in installed_packages_from_source and installed_packages_from_source[k] != v}
    new_packages = {k: v for k, v in installed_packages_from_target.items()
                    if k not in installed_packages_from_source}
    # TODO: Add support for removed packages.
    return upgrades, new_packages

