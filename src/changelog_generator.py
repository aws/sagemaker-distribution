import os

from semver import Version

from utils import get_dir_for_version, get_match_specs, get_semver


def _derive_changeset(target_version_dir, source_version_dir, image_config) -> (dict[str, list[str]], dict[str, str]):
    env_in_file_name = image_config["build_args"]["ENV_IN_FILENAME"]
    env_out_file_name = image_config["env_out_filename"]
    required_packages_from_target = get_match_specs(target_version_dir + "/" + env_in_file_name).keys()
    target_match_spec_out = get_match_specs(target_version_dir + "/" + env_out_file_name)
    source_match_spec_out = get_match_specs(source_version_dir + "/" + env_out_file_name)

    # Note: required_packages_from_source is not currently used.
    # In the future, If we remove any packages from env.in, at that time required_packages_from_source will be needed.
    # We only care about the packages which are present in the target version env.in file
    installed_packages_from_target = {
        k: str(v.get("version")).removeprefix("==")
        for k, v in target_match_spec_out.items()
        if k in required_packages_from_target
    }
    # Note: A required package in the target version might not be a required package in the source version
    # But source version could still have this package pulled as a dependency of a dependency.
    installed_packages_from_source = {
        k: str(v.get("version")).removeprefix("==")
        for k, v in source_match_spec_out.items()
        if k in required_packages_from_target
    }
    upgrades = {
        k: [installed_packages_from_source[k], v]
        for k, v in installed_packages_from_target.items()
        if k in installed_packages_from_source and installed_packages_from_source[k] != v
    }
    new_packages = {k: v for k, v in installed_packages_from_target.items() if k not in installed_packages_from_source}
    # TODO: Add support for removed packages.
    return upgrades, new_packages


def generate_change_log(target_version: Version, image_config):
    target_version_dir = get_dir_for_version(target_version)
    source_version_txt_file_path = f"{target_version_dir}/source-version.txt"
    if not os.path.exists(source_version_txt_file_path):
        print("[WARN]: Generating CHANGELOG is skipped because 'source-version.txt' isn't " "found.")
        return
    with open(source_version_txt_file_path, "r") as f:
        source_patch_version = f.readline()
    source_version = get_semver(source_patch_version)
    source_version_dir = get_dir_for_version(source_version)
    image_type = image_config["image_type"]
    upgrades, new_packages = _derive_changeset(target_version_dir, source_version_dir, image_config)
    with open(f"{target_version_dir}/CHANGELOG-{image_type}.md", "w") as f:
        f.write("# Change log: " + str(target_version) + "(" + image_type + ")\n\n")
        if len(upgrades) != 0:
            f.write("## Upgrades: \n\n")
            f.write("Package | Previous Version | Current Version\n")
            f.write("---|---|---\n")
            for package in upgrades:
                f.write(package + "|" + upgrades[package][0] + "|" + upgrades[package][1] + "\n")
        if len(new_packages) != 0:
            f.write("\n## What's new: \n\n")
            f.write("Package | Version \n")
            f.write("---|---\n")
            for package in new_packages:
                f.write(package + "|" + new_packages[package] + "\n")
