from semver import Version

_MAJOR = 'major'
_MINOR = 'minor'
_PATCH = 'patch'


def _get_dependency_upper_bound_for_runtime_upgrade(dependency_name: str, lower_bound: str, runtime_upgrade_type):
    metadata = _dependency_metadata.get(dependency_name, None)
    version_upgrade_strategy = 'semver' if metadata is None else metadata['version_upgrade_strategy']

    func = _version_upgrade_metadata[version_upgrade_strategy]['func']
    return func(lower_bound, runtime_upgrade_type)


def _get_dependency_upper_bound_for_semver(lower_bound: str, runtime_upgrade_type):
    lower_semver = Version.parse(lower_bound, optional_minor_and_patch=True)
    if runtime_upgrade_type == _MAJOR:
        return ''   # No upper bound.
    elif runtime_upgrade_type == _MINOR:
        return f'<{lower_semver.bump_major()}'
    elif runtime_upgrade_type == _PATCH:
        return f'<{lower_semver.bump_minor()}'
    else:
        raise Exception()


def _get_dependency_upper_bound_for_pythonesque(lower_bound: str, runtime_upgrade_type):
    lower_semver = Version.parse(lower_bound, optional_minor_and_patch=True)
    if runtime_upgrade_type == _MAJOR:
        return ''  # No upper bound.
    elif runtime_upgrade_type == _MINOR:
        return f'<{lower_semver.bump_minor()}'
    elif runtime_upgrade_type == _PATCH:
        return f'<{lower_semver.bump_minor()}'
    else:
        raise Exception()


_version_upgrade_metadata = {
    # Semver is a well-known version upgrade strategy. See: https://semver.org/
    #
    # Somewhat interestingly, 'calver' (see: https://calver.org/) also falls in the same category. Take Dask as an
    # example. Its versioning strategy is 'YYYY.MM.n' (where 'n' starts as 0 and increases by 1 every time a release
    # happens in the given month). So, 2nd release in December 2022 was versioned as '2022.12.1'.
    # In Amazon SageMaker Distribution, we want to move to a new month only during a minor version upgrade and new year
    # during a major version upgrade.
    'semver': {
        'func': _get_dependency_upper_bound_for_semver
    },
    # Some dependencies follow, for lack of a better word, "python style" release cycles. For e.g., even if Python does
    # a minor version upgrade from 3.9 to 3.10, we will only introduce 3.10 in Amazon SageMaker Distribution as part of
    # a major version upgrade. In other words, for dependencies below, minor version upgrades are treated as major
    # version upgrades in Amazon SageMaker Distribution.
    'pythonesque': {
        'func': _get_dependency_upper_bound_for_pythonesque
    }
}


_dependency_metadata = {
    'python': {
        'version_upgrade_strategy': 'pythonesque'
    }
}
