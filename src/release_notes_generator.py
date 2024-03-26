import os

from semver import Version

from config import _image_generator_configs
from utils import get_dir_for_version, get_match_specs


def _get_installed_packages(target_version_dir, image_config) -> dict[str, str]:
    env_in_file_name = image_config["build_args"]["ENV_IN_FILENAME"]
    env_out_file_name = image_config["env_out_filename"]
    env_in_file_path = target_version_dir + "/" + env_in_file_name
    if not os.path.exists(env_in_file_path):
        return {}
    required_packages_from_target = get_match_specs(target_version_dir + "/" + env_in_file_name).keys()
    target_match_spec_out = get_match_specs(target_version_dir + "/" + env_out_file_name)
    # We only care about the packages which are present in the target version env.in file
    return {
        k: str(v.get("version")).removeprefix("==")
        for k, v in target_match_spec_out.items()
        if k in required_packages_from_target
    }


def _get_package_to_image_type_mapping(image_type_package_metadata):
    # Creating a reverse dict based on the package names
    # { 'somepackage': {'cpu': '1.2.0', 'gpu': '1.2.2'}, ..}
    package_to_image_type_mapping = {}
    for image_type in image_type_package_metadata.keys():
        package_metadata = image_type_package_metadata[image_type]
        for package in package_metadata:
            if package not in package_to_image_type_mapping:
                package_to_image_type_mapping[package] = {image_type: package_metadata[package]}
            else:
                package_to_image_type_mapping[package][image_type] = package_metadata[package]
    return package_to_image_type_mapping


def _get_image_type_package_metadata(target_version_dir):
    image_type_package_metadata = {}
    for image_generator_config in _image_generator_configs:
        image_type_package_metadata[image_generator_config["image_type"]] = _get_installed_packages(
            target_version_dir, image_generator_config
        )
    return image_type_package_metadata


def generate_release_notes(target_version: Version):
    target_version_dir = get_dir_for_version(target_version)
    if not os.path.exists(target_version_dir):
        return
    image_type_package_metadata = _get_image_type_package_metadata(target_version_dir)
    package_to_image_type_mapping = _get_package_to_image_type_mapping(image_type_package_metadata)

    with open(f"{target_version_dir}/RELEASE.md", "w") as f:
        f.write("# Release notes: " + str(target_version) + "\n\n")
        f.write("Package ")
        table_separator = "---"
        for image_type in image_type_package_metadata.keys():
            f.write("| " + image_type)
            table_separator += "|---"
        f.write("\n")
        f.write(table_separator + "\n")
        for package in package_to_image_type_mapping.keys():
            f.write(package)
            for image_type in image_type_package_metadata.keys():
                version = (
                    package_to_image_type_mapping[package][image_type]
                    if image_type in package_to_image_type_mapping[package]
                    else " "
                )
                f.write("|" + version)
            f.write("\n")
