import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional

from conda.env.specs.requirements import RequirementsSpec
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
    return container_log_content.replace(b"%21", b"!")


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


def read_env_file(file_path):
    """Read environment file using conda's RequirementsSpec"""
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


def conda_search_with_retry(command, package, max_retries=5, base_delay=1):
    """
    Retry conda search command with exponential backoff for utils
    """
    for attempt in range(max_retries):
        try:
            search_result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
            return search_result
        except subprocess.TimeoutExpired:
            if attempt == max_retries - 1:
                print(f"Timeout searching for package {package} after {max_retries} attempts, ignore.")
                return None
            delay = base_delay * (2**attempt)
            time.sleep(delay)
        except subprocess.CalledProcessError as e:
            if attempt == max_retries - 1:
                print(f"Error searching for package {package} after {max_retries} attempts: {str(e)}")
                return None
            delay = base_delay * (2**attempt)
            time.sleep(delay)
    return None


def _search_single_package(package: str, match_spec_out) -> tuple[str, Optional[dict]]:
    """
    Search for a single package metadata using conda search with retry logic
    """
    package_version = str(match_spec_out.get("version")).removeprefix("==")
    channel = match_spec_out.get("channel").channel_name

    command = ["conda", "search", "-c", channel, f"{package}=={package_version}", "--json"]

    search_result = conda_search_with_retry(command, package)
    if search_result is None:
        return package, None

    try:
        package_metadata = json.loads(search_result.stdout)[package][0]
        result = {"version": package_metadata["version"], "size": package_metadata["size"]}
        return package, result
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing search result for package {package}: {str(e)}")
        return package, None


def pull_conda_package_metadata(image_config, image_artifact_dir, max_workers: int = 20):
    """
    Pull conda package metadata using parallel conda search calls for improved performance
    """
    results = dict()
    env_out_file_name = image_config["env_out_filename"]
    match_spec_out = get_match_specs(image_artifact_dir + "/" + env_out_file_name)

    conda_forge_packages = [
        (package, match_spec_out)
        for package, match_spec_out in match_spec_out.items()
        if str(match_spec_out).startswith("conda-forge")
    ]

    if not conda_forge_packages:
        print("No conda-forge packages found")
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_package = {
            executor.submit(_search_single_package, package, match_spec): package
            for package, match_spec in conda_forge_packages
        }

        for future in as_completed(future_to_package):
            try:
                package_name, package_metadata = future.result()
                if package_metadata:
                    results[package_name] = package_metadata

            except Exception as e:
                print(f"Unexpected error processing package: {e}")

    results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]["size"], reverse=True)}

    return results


def _get_version(match_spec) -> str:
    return str(match_spec.get("version")).removeprefix("==")


@dataclass
class DependencyChanges:
    changed: dict[str, tuple[str, str]] = field(default_factory=dict)
    added: dict[str, str] = field(default_factory=dict)
    removed: dict[str, str] = field(default_factory=dict)


@dataclass
class Changeset:
    direct: DependencyChanges = field(default_factory=DependencyChanges)
    indirect: DependencyChanges = field(default_factory=DependencyChanges)


def _derive_direct_changes(
    source_out: dict,
    target_out: dict,
    direct_in_source: set,
    direct_in_target: set,
    promoted: set[str],
    demoted: set[str],
) -> DependencyChanges:
    """Compute changes for packages explicitly listed in env.in (direct dependencies).

    Promoted packages (indirect→direct) appear in changed if their version changed, otherwise
    silently skipped. Demoted packages (direct→indirect) are excluded entirely from this section.
    """
    target_versions = {k: _get_version(v) for k, v in target_out.items() if k in direct_in_target}
    source_versions = {k: _get_version(v) for k, v in source_out.items()}

    changed = {
        k: [source_versions[k], v]
        for k, v in target_versions.items()
        if k in source_versions and source_versions[k] != v
    }

    # Exclude promoted — they weren't truly "added" (already in the image)
    added = {k: v for k, v in target_versions.items() if k not in source_versions and k not in promoted}

    # Only fully removed packages (demoted ones stay in the image, just move to indirect)
    removed = {
        k: _get_version(v)
        for k, v in source_out.items()
        if k in direct_in_source and k not in target_out and k not in demoted
    }

    return DependencyChanges(changed=changed, added=added, removed=removed)


def _derive_indirect_changes(
    source_out: dict,
    target_out: dict,
    direct_in_source: set,
    direct_in_target: set,
    promoted: set[str],
    demoted: set[str],
) -> DependencyChanges:
    """Compute changes for transitive packages (present in env.out but not env.in).

    Demoted packages (direct→indirect) appear in changed if their version changed, otherwise
    silently skipped. Promoted packages (indirect→direct) are excluded entirely from this section.
    """
    source_versions = {k: _get_version(v) for k, v in source_out.items() if k not in direct_in_source}
    target_versions = {k: _get_version(v) for k, v in target_out.items() if k not in direct_in_target}

    # Include demoted packages in version comparison using their source versions
    source_versions_for_change = {
        **source_versions,
        **{k: _get_version(v) for k, v in source_out.items() if k in demoted},
    }

    changed = {
        k: [source_versions_for_change[k], v]
        for k, v in target_versions.items()
        if k in source_versions_for_change and source_versions_for_change[k] != v
    }

    # Exclude demoted — they weren't truly "added" (already in the image)
    added = {k: v for k, v in target_versions.items() if k not in source_versions_for_change and k not in demoted}

    # Exclude promoted — they moved to direct and are shown there (if version changed)
    removed = {k: v for k, v in source_versions.items() if k not in target_versions and k not in promoted}

    return DependencyChanges(changed=changed, added=added, removed=removed)


def derive_changeset(source_version_dir, target_version_dir, image_config) -> Changeset:
    env_in_file_name = image_config["build_args"]["ENV_IN_FILENAME"]
    env_out_file_name = image_config["env_out_filename"]

    direct_in_source = set(get_match_specs(source_version_dir + "/" + env_in_file_name).keys())
    direct_in_target = set(get_match_specs(target_version_dir + "/" + env_in_file_name).keys())
    source_out = get_match_specs(source_version_dir + "/" + env_out_file_name)
    target_out = get_match_specs(target_version_dir + "/" + env_out_file_name)

    # Promoted: indirect in source (in source_out but not direct_in_source), now direct in target
    promoted = {k for k in direct_in_target if k in source_out and k not in direct_in_source}

    # Demoted: direct in source, no longer direct in target, but still present transitively
    demoted = {k for k in direct_in_source if k not in direct_in_target and k in target_out}

    return Changeset(
        direct=_derive_direct_changes(source_out, target_out, direct_in_source, direct_in_target, promoted, demoted),
        indirect=_derive_indirect_changes(
            source_out, target_out, direct_in_source, direct_in_target, promoted, demoted
        ),
    )
