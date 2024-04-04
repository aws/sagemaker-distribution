import json
import os

import conda.cli.python_api
from conda.models.match_spec import MatchSpec

from config import _image_generator_configs
from dependency_upgrader import _dependency_metadata
from utils import get_dir_for_version, get_match_specs, get_semver, sizeof_fmt


def _get_package_versions_in_upstream(target_packages_match_spec_out, target_version) -> dict[str, str]:
    package_to_version_mapping = {}
    is_major_version_release = target_version.minor == 0 and target_version.patch == 0
    is_minor_version_release = target_version.patch == 0 and not is_major_version_release
    for package in target_packages_match_spec_out:
        # Execute a conda search api call in the linux-64 subdirectory
        # packages such as pytorch-gpu are present only in linux-64 sub directory
        match_spec_out = target_packages_match_spec_out[package]
        package_version = str(match_spec_out.get("version")).removeprefix("==")
        package_version = get_semver(package_version)
        channel = match_spec_out.get("channel").channel_name
        subdir_filter = "[subdir=" + match_spec_out.get("subdir") + "]"
        search_result = conda.cli.python_api.run_command(
            "search", channel + "::" + package + ">=" + str(package_version) + subdir_filter, "--json"
        )
        # Load the first result as json. The API sends a json string inside an array
        package_metadata = json.loads(search_result[0])[package]
        # Response is of the structure
        # { 'package_name': [{'url':<someurl>, 'dependencies': <List of dependencies>, 'version':
        # <version number>}, ..., {'url':<someurl>, 'dependencies': <List of dependencies>, 'version':
        # <version number>}]
        # We only care about the version number in the last index
        package_version_in_conda = ""
        if is_major_version_release:
            latest_package_version_in_conda = package_metadata[-1]["version"]
        elif is_minor_version_release:
            package_major_version_prefix = str(package_version.major) + "."
            latest_package_version_in_conda = [
                x["version"] for x in package_metadata if x["version"].startswith(package_major_version_prefix)
            ][-1]
        else:
            package_minor_version_prefix = ".".join([str(package_version.major), str(package_version.minor)]) + "."
            latest_package_version_in_conda = [
                x["version"] for x in package_metadata if x["version"].startswith(package_minor_version_prefix)
            ][-1]

        package_to_version_mapping[package] = latest_package_version_in_conda
    return package_to_version_mapping


def _generate_staleness_report_per_image(
    package_versions_in_upstream, target_packages_match_spec_out, image_config, version
):
    print("\n# Staleness Report: " + str(version) + "(" + image_config["image_type"] + ")\n")
    print("Package | Current Version in the Distribution image | Latest Relevant Version in " "Upstream")
    print("---|---|---")
    for package in package_versions_in_upstream:
        version_in_sagemaker_distribution = str(target_packages_match_spec_out[package].get("version")).removeprefix(
            "=="
        )
        if version_in_sagemaker_distribution == package_versions_in_upstream[package]:
            print(package + "|" + version_in_sagemaker_distribution + "|" + package_versions_in_upstream[package])
        else:
            print(
                "${\color{red}"
                + package
                + "}$"
                + "|"
                + version_in_sagemaker_distribution
                + "|"
                + package_versions_in_upstream[package]
            )


def _get_installed_package_versions_and_conda_versions(
    image_config, target_version_dir, target_version
) -> (dict[str, MatchSpec], dict[str, str]):
    env_in_file_name = image_config["build_args"]["ENV_IN_FILENAME"]
    env_out_file_name = image_config["env_out_filename"]
    required_packages_from_target = get_match_specs(target_version_dir + "/" + env_in_file_name).keys()
    match_spec_out = get_match_specs(target_version_dir + "/" + env_out_file_name)
    # We only care about packages which are present in env.in
    # Remove Python from the dictionary, we don't want to track python version as part of our
    # staleness report.
    target_packages_match_spec_out = {
        k: v for k, v in match_spec_out.items() if k in required_packages_from_target and k not in _dependency_metadata
    }
    latest_package_versions_in_upstream = _get_package_versions_in_upstream(
        target_packages_match_spec_out, target_version
    )
    return target_packages_match_spec_out, latest_package_versions_in_upstream


def _generate_python_package_size_report_per_image(
    base_version_dir, target_version_dir, image_config, base_version, target_version
):
    print("\n# Python Package Size Report " + "(" + image_config["image_type"].upper() + ")\n")
    print("\n### Target Version: " + str(target_version) + " | Base Version:" + str(base_version) + "\n")
    target_pkg_metadata_file = f'{target_version_dir}/{image_config["package_metadata_filename"]}'
    base_pkg_metadata_file = f'{base_version_dir}/{image_config["package_metadata_filename"]}'
    if not os.path.exists(target_pkg_metadata_file):
        raise Exception("No Python package metadata file found for target version, please try re-build the image.")
    with open(target_pkg_metadata_file) as jsonfile:
        target_pkg_metadata = json.load(jsonfile)
    base_pkg_metadata = None
    base_total_size = None
    if not os.path.exists(base_pkg_metadata_file):
        print("WARNING: No Python package metadata file found for base version, only partial results will be shown.")
    else:
        with open(base_pkg_metadata_file) as jsonfile:
            base_pkg_metadata = json.load(jsonfile)
        base_total_size = sum(d["size"] for d in base_pkg_metadata.values())

    # Print out the total size change of all Python packages in the image.
    target_total_size = sum(d["size"] for d in target_pkg_metadata.values())
    total_size_delta_val = (target_total_size - base_total_size) if base_total_size else None
    total_size_delta_rel = (total_size_delta_val / base_total_size) if base_total_size else None
    print("\n## Python Packages Total Size Delta\n")
    print("Target Version Total Size | Base Version Total Size | Size Change (abs) | Size Change (%)")
    print("---|---|---|---")
    print(
        sizeof_fmt(target_total_size)
        + "|"
        + (sizeof_fmt(base_total_size) if base_total_size else "-")
        + "|"
        + (sizeof_fmt(total_size_delta_val) if total_size_delta_val else "-")
        + "|"
        + (str(round(total_size_delta_rel * 100, 2)) if total_size_delta_rel else "-")
    )

    # Print out the largest 20 Python packages in the image, sorted decending by size.
    print("\n## Top-20 Largest Python Packages\n")
    print("Package | Version in the Target Image | Size")
    print("---|---|---")

    for i, (k, v) in enumerate(target_pkg_metadata.items()):
        if i >= 20:
            break
        print(k + "|" + v["version"] + "|" + sizeof_fmt(v["size"]))

    # Print out the size delta for each changed/new package in the image, sorted decending by size.
    if base_pkg_metadata:
        print("\n## Python Package Size Delta\n")
        print("Package | Version in the Target Image | Version in the Base Image | Size Change (abs) | Size Change (%)")
        print("---|---|---|---|---")
        package_size_delta_dict = dict()
        for k, v in target_pkg_metadata.items():
            if k not in base_pkg_metadata or base_pkg_metadata[k]["version"] != v["version"]:
                base_pkg_size = base_pkg_metadata[k]["size"] if k in base_pkg_metadata else 0
                size_delta_abs = v["size"] - base_pkg_size
                package_size_delta_dict[k] = {
                    "target_version": v["version"],
                    "base_version": base_pkg_metadata[k]["version"] if k in base_pkg_metadata else "-",
                    "size_delta_abs": size_delta_abs,
                    "size_delta_rel": (size_delta_abs / base_pkg_size) if base_pkg_size else None,
                }
        # Sort the package size delta based on absolute size diff in decending order.
        package_size_delta_dict = {
            k: v
            for k, v in sorted(
                package_size_delta_dict.items(), key=lambda item: item[1]["size_delta_abs"], reverse=True
            )
        }

        for k, v in package_size_delta_dict.items():
            print(
                k
                + "|"
                + v["target_version"]
                + "|"
                + v["base_version"]
                + "|"
                + sizeof_fmt(v["size_delta_abs"])
                + "|"
                + (str(round(v["size_delta_rel"] * 100, 2)) if v["size_delta_rel"] else "-")
            )


def generate_package_staleness_report(args):
    target_version = get_semver(args.target_patch_version)
    target_version_dir = get_dir_for_version(target_version)
    for image_config in _image_generator_configs:
        (
            target_packages_match_spec_out,
            latest_package_versions_in_upstream,
        ) = _get_installed_package_versions_and_conda_versions(image_config, target_version_dir, target_version)
        _generate_staleness_report_per_image(
            latest_package_versions_in_upstream, target_packages_match_spec_out, image_config, target_version
        )


def generate_package_size_report(args):
    target_version = get_semver(args.target_patch_version)
    target_version_dir = get_dir_for_version(target_version)

    base_version = get_semver(args.base_patch_version)
    base_version_dir = get_dir_for_version(base_version)
    for image_config in _image_generator_configs:
        _generate_python_package_size_report_per_image(
            base_version_dir, target_version_dir, image_config, base_version, target_version
        )
