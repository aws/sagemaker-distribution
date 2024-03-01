from __future__ import absolute_import

import pytest

pytestmark = pytest.mark.unit
from dependency_upgrader import (
    _get_dependency_upper_bound_for_runtime_upgrade,
    _get_dependency_upper_bound_for_semver,
    _get_dependency_upper_bound_for_pythonesque,
    _MAJOR,
    _MINOR,
    _PATCH
)


def test_get_dependency_upper_bound_for_runtime_upgrade():
    # case 1: Runtime upgrade type is MINOR, dependency name is python => use pythonesque
    assert _get_dependency_upper_bound_for_runtime_upgrade('python', '1.2.5', _MINOR) == ',<1.3.0'
    # case 1: Runtime upgrade type is MINOR, dependency name is node => use semver
    assert _get_dependency_upper_bound_for_runtime_upgrade('node', '1.2.5', _MINOR) == ',<2.0.0'


def test_get_dependency_upper_bound_for_semver():
    # case 1: Runtime upgrade type is MAJOR.
    assert _get_dependency_upper_bound_for_semver('1.2.5', _MAJOR) == ''
    # case 2: Runtime upgrade type is MINOR.
    assert _get_dependency_upper_bound_for_semver('1.2.5', _MINOR) == ',<2.0.0'
    # case 3: Runtime upgrade type is PATCH.
    assert _get_dependency_upper_bound_for_semver('1.2.5', _PATCH) == ',<1.3.0'
    # case 4: Throw exception for any other runtime_upgrade_type
    with pytest.raises(Exception):
        _get_dependency_upper_bound_for_semver('1.2.5', 'prerelease')


def test_get_dependency_upper_bound_for_pythonesque():
    # case 1: Runtime upgrade type is MAJOR.
    assert _get_dependency_upper_bound_for_pythonesque('1.2.5', _MAJOR) == ''
    # case 2: Runtime upgrade type is MINOR.
    assert _get_dependency_upper_bound_for_pythonesque('1.2.5', _MINOR) == ',<1.3.0'
    # case 3: Runtime upgrade type is PATCH. For pythonesque, we will bump minor version.
    assert _get_dependency_upper_bound_for_pythonesque('1.2.5', _PATCH) == ',<1.3.0'
    # case 4: Throw exception for any other runtime_upgrade_type
    with pytest.raises(Exception):
        _get_dependency_upper_bound_for_pythonesque('1.2.5', 'prerelease')


def test_get_dependency_upper_bound_for_post_pre_release():
    assert _get_dependency_upper_bound_for_runtime_upgrade('python', '1.2.5.post1', _PATCH) == ',<1.3.0'
    assert _get_dependency_upper_bound_for_runtime_upgrade('node', '1.2.5.post1', _PATCH) == ',<1.3.0'
    assert _get_dependency_upper_bound_for_runtime_upgrade('python', '1.2.5.post1', _MINOR) == ',<1.3.0'
    assert _get_dependency_upper_bound_for_runtime_upgrade('node', '1.2.5.post1', _MINOR) == ',<2.0.0'
    assert _get_dependency_upper_bound_for_runtime_upgrade('python', '1.2.5.post1', _MAJOR) == ''
    assert _get_dependency_upper_bound_for_runtime_upgrade('node', '1.2.5.post1', _MAJOR) == ''
