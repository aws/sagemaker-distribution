import json
import os
from itertools import islice

import boto3
import conda.cli.python_api
from conda.models.match_spec import MatchSpec

from config import _image_generator_configs
from dependency_upgrader import _dependency_metadata
from utils import (
    create_markdown_table,
    derive_changeset,
    get_dir_for_version,
    get_match_specs,
    get_semver,
    pull_conda_package_metadata,
    sizeof_fmt,
)


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
            package_minor_version_prefix = ".".join([str(package_version.major), str(package_version.minor)])
            latest_package_version_in_conda = [
                x["version"] for x in package_metadata if x["version"].startswith(package_minor_version_prefix)
            ][-1]

        package_to_version_mapping[package] = latest_package_version_in_conda
    return package_to_version_mapping


def _generate_staleness_report_per_image(
    package_versions_in_upstream, target_packages_match_spec_out, image_config, version
):
    print("\n# Staleness Report: " + str(version) + "(" + image_config["image_type"] + ")\n")
    staleness_report_rows = []
    for package in package_versions_in_upstream:
        version_in_sagemaker_distribution = str(target_packages_match_spec_out[package].get("version")).removeprefix(
            "=="
        )
        package_string = (
            package
            if version_in_sagemaker_distribution == package_versions_in_upstream[package]
            else "${\color{red}" + package + "}$"
        )
        staleness_report_rows.append(
            {
                "package": package_string,
                "version_in_sagemaker_distribution": version_in_sagemaker_distribution,
                "latest_relavant_version": package_versions_in_upstream[package],
            }
        )
    print(
        create_markdown_table(
            ["Package", "Current Version in the Distribution image", "Latest Relevant Version in " "Upstream"],
            staleness_report_rows,
        )
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


def _validate_new_package_size(new_package_total_size, target_total_size, image_type, target_version):
    # Validate if the new packages account for <= 5% of the total python package size of target image.
    new_package_total_size_percent_threshold = 5
    validate_result = None
    new_package_total_size_percent = round(new_package_total_size / target_total_size * 100, 2)
    new_package_total_size_percent_string = str(new_package_total_size_percent)
    if new_package_total_size_percent > new_package_total_size_percent_threshold:
        validate_result = (
            "The total size of newly introduced Python packages accounts for more than "
            + str(new_package_total_size_percent_threshold)
            + "% of the total Python package size of "
            + image_type
            + " image, version "
            + str(target_version)
            + "! ("
            + str(new_package_total_size_percent)
            + "%)"
        )
        new_package_total_size_percent_string = "${\color{red}" + str(new_package_total_size_percent) + "}$"

    print(
        "The total size of newly introduced Python packages is "
        + sizeof_fmt(new_package_total_size)
        + ", accounts for "
        + new_package_total_size_percent_string
        + "% of the total package size."
    )
    return validate_result


def _generate_python_package_size_report_per_image(
    base_pkg_metadata, target_pkg_metadata, image_config, base_version, target_version
):
    validate_result = None
    image_type = image_config["image_type"].upper()
    print("\n# Python Package Size Report " + "(" + image_type + ")\n")
    print("\n### Target Image Version: " + str(target_version) + " | Base Image Version: " + str(base_version) + "\n")
    if not base_pkg_metadata or not base_version:
        print("WARNING: No Python package metadata file found for base image, only partial results will be shown.")
    base_total_size = sum(d["size"] for d in base_pkg_metadata.values()) if base_pkg_metadata else None

    # Print out the total size change of all Python packages in the image.
    target_total_size = sum(d["size"] for d in target_pkg_metadata.values())
    total_size_delta_val = (target_total_size - base_total_size) if base_total_size else None
    total_size_delta_rel = (total_size_delta_val / base_total_size) if base_total_size else None
    print("\n## Python Packages Total Size Summary\n")
    print(
        create_markdown_table(
            ["Target Version Total Size", "Base Version Total Size", "Size Change (abs)", "Size Change (%)"],
            [
                {
                    "target_total_size": sizeof_fmt(target_total_size),
                    "base_total_size": sizeof_fmt(base_total_size) if base_total_size else "-",
                    "size_delta_val": sizeof_fmt(total_size_delta_val) if total_size_delta_val else "-",
                    "size_delta_rel": str(round(total_size_delta_rel * 100, 2)) if total_size_delta_rel else "-",
                }
            ],
        )
    )

    # Print out the largest 20 Python packages in the image, sorted decending by size.
    print("\n## Top-20 Largest Python Packages\n")
    print(
        create_markdown_table(
            ["Package", "Version in the Target Image", "Size"],
            [
                {"pkg": k, "version": v["version"], "size": sizeof_fmt(v["size"])}
                for k, v in islice(target_pkg_metadata.items(), None, 20)
            ],
        )
    )

    # Print out the size delta for each changed/new package in the image, sorted decending by size.
    if base_pkg_metadata:
        print("\n## Python Package Size Delta\n")
        new_package_total_size = 0
        package_size_delta_list = []
        for k, v in target_pkg_metadata.items():
            if k not in base_pkg_metadata or base_pkg_metadata[k]["version"] != v["version"]:
                base_pkg_size = base_pkg_metadata[k]["size"] if k in base_pkg_metadata else 0
                size_delta_abs = v["size"] - base_pkg_size
                package_size_delta_list.append(
                    {
                        "package": k,
                        "target_version": v["version"],
                        "base_version": base_pkg_metadata[k]["version"] if k in base_pkg_metadata else "-",
                        "size_delta_abs": size_delta_abs,
                        "size_delta_rel": (size_delta_abs / base_pkg_size) if base_pkg_size else None,
                    }
                )
                if k not in base_pkg_metadata:
                    new_package_total_size += v["size"]
        # Sort the package size delta based on absolute size diff in decending order.
        package_size_delta_list = sorted(package_size_delta_list, key=lambda item: item["size_delta_abs"], reverse=True)
        for v in package_size_delta_list:
            v["size_delta_rel"] = str(round(v["size_delta_rel"] * 100, 2)) if v["size_delta_rel"] else "-"
            v["size_delta_abs"] = sizeof_fmt(v["size_delta_abs"])

        validate_result = _validate_new_package_size(
            new_package_total_size, target_total_size, image_type, target_version
        )
        print(
            create_markdown_table(
                [
                    "Package",
                    "Version in the Target Image",
                    "Version in the Base Image",
                    "Size Change (abs)",
                    "Size Change (%)",
                ],
                package_size_delta_list,
            )
        )
    return validate_result


def _generate_python_package_dependency_report(image_config, base_version_dir, target_version_dir):
    # Get a list of newly introduced marquee packages in changeset and their versions.
    _, new_packages = derive_changeset(target_version_dir, base_version_dir, image_config)

    results = dict()
    for package, version in new_packages.items():
        # Pull package metadata from conda-forge and dump into json file
        search_result = conda.cli.python_api.run_command("search", f"{package}=={version}", "--json")
        package_metadata = json.loads(search_result[0])[package][0]
        results[package] = {"version": package_metadata["version"], "depends": package_metadata["depends"]}

    print(
        create_markdown_table(
            ["Package", "Version in the Target Image", "Dependencies"],
            [
                {"pkg": k, "version": v["version"], "depends": v["depends"]}
                for k, v in islice(results.items(), None, 20)
            ],
        )
    )


def generate_package_staleness_report(args):
    target_version = get_semver(args.target_patch_version)
    target_version_dir = get_dir_for_version(target_version)
    for image_config in _image_generator_configs[target_version.major]:
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

    base_version = None
    source_version_txt_file_path = f"{target_version_dir}/source-version.txt"
    if os.path.exists(source_version_txt_file_path):
        with open(source_version_txt_file_path, "r") as f:
            source_patch_version = f.readline()
        base_version = get_semver(source_patch_version)
    base_version_dir = get_dir_for_version(base_version) if base_version else None

    # Generate the report for Total Image Size changed from Base Version
    _generate_image_size_report(target_version, base_version, args.staging_repo_name, args.staging_account)

    validate_results = []
    for image_config in _image_generator_configs[target_version.major]:
        base_pkg_metadata = pull_conda_package_metadata(image_config, base_version_dir) if base_version else None
        target_pkg_metadata = pull_conda_package_metadata(image_config, target_version_dir)

        validate_result = _generate_python_package_size_report_per_image(
            base_pkg_metadata, target_pkg_metadata, image_config, base_version, target_version
        )
        if validate_result:
            validate_results.append(validate_result)

    if args.validate:
        if validate_results:
            raise Exception(f"Size Validation Failed! Issues found: {validate_results}")
        print("Pakcage Size Validation Passed!")


def generate_package_dependency_report(args):
    target_version = get_semver(args.target_patch_version)
    target_version_dir = get_dir_for_version(target_version)

    base_version = None
    source_version_txt_file_path = f"{target_version_dir}/source-version.txt"
    if os.path.exists(source_version_txt_file_path):
        with open(source_version_txt_file_path, "r") as f:
            source_patch_version = f.readline()
        base_version = get_semver(source_patch_version)

    base_version_dir = get_dir_for_version(base_version) if base_version else None

    print("\n# Python Package Dependency Report\n")
    print("\n### Target Image Version: " + str(target_version) + " | Base Image Version: " + str(base_version) + "\n")
    if not base_version:
        print("WARNING: No base version or base version directory found, will generate full report for target version.")
    for _, configs in _image_generator_configs.items():
        for image_config in configs:
            print("## Image Type: " + "(" + image_config["image_type"].upper() + ")")
            _generate_python_package_dependency_report(image_config, base_version_dir, target_version_dir)


def get_image_size(image_tag, staging_repo_name, staging_account):
    try:
        ecr_client = boto3.client("ecr", region_name="us-east-1")

        response = ecr_client.describe_images(
            registryId=staging_account, repositoryName=staging_repo_name, imageIds=[{"imageTag": image_tag}]
        )
        image_details = response.get("imageDetails", [])
        if image_details:
            image_size_bytes = image_details[0].get("imageSizeInBytes")
            if image_size_bytes:
                image_size_gb = image_size_bytes / (1024**3)
                return image_size_gb
            else:
                print(f"Image size not found for {staging_repo_name}:{image_tag}")
        else:
            print(f"No image details found for {staging_repo_name}:{image_tag}")

    except Exception as e:
        print(f"Error retrieving image size: {str(e)}")

    return None


def _generate_image_size_report(target_version, base_version, staging_repo_name, staging_account):
    target_tag_gpu = f"{target_version.major}.{target_version.minor}.{target_version.patch}-gpu"
    base_tag_gpu = f"{base_version.major}.{base_version.minor}.{base_version.patch}-gpu" if base_version else None

    target_tag_cpu = f"{target_version.major}.{target_version.minor}.{target_version.patch}-cpu"
    base_tag_cpu = f"{base_version.major}.{base_version.minor}.{base_version.patch}-cpu" if base_version else None

    target_size_gpu = get_image_size(target_tag_gpu, staging_repo_name, staging_account)
    base_size_gpu = get_image_size(base_tag_gpu, staging_repo_name, staging_account) if base_tag_gpu else None

    target_size_cpu = get_image_size(target_tag_cpu, staging_repo_name, staging_account)
    base_size_cpu = get_image_size(base_tag_cpu, staging_repo_name, staging_account) if base_tag_cpu else None

    headers = ["Target Image Size", "Base Image Size", "Size Difference", "Size Change (%)"]

    print("\n# GPU Total Image Size Report\n")
    if target_size_gpu is not None and base_size_gpu is not None:
        size_diff_gpu = target_size_gpu - base_size_gpu
        size_diff_gpu_rel = size_diff_gpu / base_size_gpu if base_size_gpu != 0 else 0

        size_change_gpu = f"{size_diff_gpu:.2f} GB {'Larger' if size_diff_gpu > 0 else ('Smaller' if size_diff_gpu < 0 else 'No Change')}"

        size_change_percentage_gpu = (
            f"{round(abs(size_diff_gpu_rel * 100), 2)}% {'Larger' if size_diff_gpu > 0 else ('Smaller' if size_diff_gpu < 0 else 'No Change')}"
            if size_diff_gpu_rel
            else "-"
        )

        rows = [
            {
                "Target Image Size": f"{target_tag_gpu}:{target_size_gpu:.2f} GB",
                "Base Image Size": f"{base_tag_gpu}:{base_size_gpu:.2f} GB",
                "Size Difference": size_change_gpu,
                "Size Change (%)": size_change_percentage_gpu,
            }
        ]
        print(create_markdown_table(headers, rows))
    else:
        print(f"Failed to retrieve size for target image: {target_tag_gpu} or base image: {base_tag_gpu}")

    print("\n# CPU Total Image Size Report\n")
    if target_size_cpu is not None and base_size_cpu is not None:
        size_diff_cpu = target_size_cpu - base_size_cpu
        size_diff_cpu_rel = size_diff_cpu / base_size_cpu if base_size_cpu != 0 else 0

        size_change_cpu = f"{size_diff_cpu:.2f} GB {'Larger' if size_diff_cpu > 0 else ('Smaller' if size_diff_cpu < 0 else 'No Change')}"

        size_change_percentage_cpu = (
            f"{round(abs(size_diff_cpu_rel * 100), 2)}% {'Larger' if size_diff_cpu > 0 else ('Smaller' if size_diff_cpu < 0 else 'No Change')}"
            if size_diff_cpu_rel
            else "-"
        )

        rows = [
            {
                "Target Image Size": f"{target_tag_cpu}:{target_size_cpu:.2f} GB",
                "Base Image Size": f"{base_tag_cpu}:{base_size_cpu:.2f} GB",
                "Size Difference": size_change_cpu,
                "Size Change (%)": size_change_percentage_cpu,
            }
        ]
        print(create_markdown_table(headers, rows))
    else:
        print(f"Failed to retrieve size for target image: {target_tag_cpu} or base image: {base_tag_cpu}")
