import os

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
