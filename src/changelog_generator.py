import os

from semver import Version

from utils import derive_changeset, get_dir_for_version, get_semver


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
    upgrades, new_packages = derive_changeset(target_version_dir, source_version_dir, image_config)
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
