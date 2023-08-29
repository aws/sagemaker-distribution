import os
from semver import Version
from conda.models.match_spec import MatchSpec
from conda_env.specs import RequirementsSpec


def get_dir_for_version(version: Version) -> str:
    version_prerelease_suffix = f'/v{version.major}.{version.minor}.{version.patch}-' \
                                f'{version.prerelease}' if version.prerelease else ''
    return os.path.relpath(f'build_artifacts/v{version.major}/v{version.major}.{version.minor}/'
                           f'v{version.major}.{version.minor}.{version.patch}'
                           f'{version_prerelease_suffix}')


def is_exists_dir_for_version(version: Version) -> bool:
    dir_path = get_dir_for_version(version)
    # Also validate whether this directory is not generated due to any pre-release builds
    # This can be validated by checking whether {cpu/gpu}.env.{in/out}/Dockerfile exists in the
    # directory.
    return os.path.exists(dir_path) and os.path.exists(dir_path + "/" + 'Dockerfile')


def get_semver(version_str) -> Version:
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
    assert 'conda' in requirement_spec.environment.dependencies

    return {MatchSpec(i).get('name'): MatchSpec(i) for i in
            requirement_spec.environment.dependencies['conda']}
