import json
import os

import conda.cli.python_api
from conda.env.specs import RequirementsSpec
from conda.models.match_spec import MatchSpec
from semver import Version


def get_dir_for_version(version: Version) -> str:
    version_prerelease_suffix = (
        f"/v{version.major}.{version.minor}.{version.patch}-" f"{version.prerelease}" if version.prerelease else ""
    )
    return os.path.relpath(
        f"build_artifacts/v{version.major}/v{version.major}.{version.minor}/"
        f"v{version.major}.{version.minor}.{version.patch}"
        f"{version_prerelease_suffix}"
    )


# Clean versioning strings
def post_handle_container_log(container_log_content):
    # Work with bytes directly
    return container_log_content.replace(b'%21', b'!')


def is_exists_dir_for_version(version: Version, file_name_to_verify_existence="Dockerfile") -> bool:
    dir_path = get_dir_for_version(version)
    # Also validate whether this directory is not generated due to any pre-release builds/
    # additional packages.
    # This can be validated by checking whether {cpu/gpu}.env.{in/out}/Dockerfile exists in the
    # directory.
    return os.path.exists(dir_path) and os.path.exists(dir_path + "/" + file_name_to_verify_existence)


def get_semver(version_str) -> Version:
    # Version strings on conda-forge follow PEP standards rather than SemVer, which support
    # version strings such as X.Y.Z.postN, X.Y.Z.preN. These cause errors in semver.Version.parse
    # so we keep the first 3 entries as version string.
    if version_str.count(".") > 2:
        version_str = ".".join(version_str.split(".")[:3])
    elif version_str.count(".") == 1:
        version_str = version_str + ".0"
    version = Version.parse(version_str)
    if version.build is not None:
        raise Exception()
    return version


def read_env_file(file_path) -> RequirementsSpec:
    return RequirementsSpec(filename=file_path)


def get_match_specs(file_path) -> dict[str, MatchSpec]:
    if not os.path.isfile(file_path):
        return {}

    requirement_spec = read_env_file(file_path)
    assert len(requirement_spec.environment.dependencies) == 1
    assert "conda" in requirement_spec.environment.dependencies

    return {MatchSpec(i).get("name"): MatchSpec(i) for i in requirement_spec.environment.dependencies["conda"]}


def sizeof_fmt(num):
    # Convert byte to human-readable size units.
    for unit in ("B", "KB", "MB", "GB"):
        if abs(num) < 1024.0:
            return f"{num:3.2f}{unit}"
        num /= 1024.0
    return f"{num:.2f}TB"


def create_markdown_table(headers, rows):
    """Loop through a data rows and return a markdown table as a multi-line string.

    headers -- A list of strings, each string represents a column name
    rows -- A list of dicts, each dict is a row
    """
    markdowntable = ""
    # Make a string of all the keys in the first dict with pipes before after and between each key
    markdownheader = " | ".join(headers)
    # Make a header separator line with dashes instead of key names
    markdownheaderseparator = "---|" * (len(headers) - 1) + "---"
    # Add the header row and separator to the table
    markdowntable += markdownheader + "\n"
    markdowntable += markdownheaderseparator + "\n"
    # Loop through the list of dictionaries outputting the rows
    for row in rows:
        markdownrow = ""
        for k, v in row.items():
            markdownrow += str(v) + "|"
        markdowntable += markdownrow[:-1] + "\n"
    return markdowntable


def pull_conda_package_metadata(image_config, image_artifact_dir):
    results = dict()
    env_out_file_name = image_config["env_out_filename"]
    match_spec_out = get_match_specs(image_artifact_dir + "/" + env_out_file_name)

    target_packages_match_spec_out = {k: v for k, v in match_spec_out.items()}

    for package, match_spec_out in target_packages_match_spec_out.items():
        if str(match_spec_out).startswith("conda-forge"):
            # Pull package metadata from conda-forge and dump into json file
            search_result = conda.cli.python_api.run_command("search", str(match_spec_out), "--json")
            package_metadata = json.loads(search_result[0])[package][0]
            results[package] = {"version": package_metadata["version"], "size": package_metadata["size"]}
    # Sort the pakcage sizes in decreasing order
    results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]["size"], reverse=True)}

    return results


def derive_changeset(target_version_dir, source_version_dir, image_config) -> (dict[str, list[str]], dict[str, str]):
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
