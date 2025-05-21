import json
from unittest.mock import Mock, patch

import pytest
from nightly_build_helper import NightlyBuildHelper

pytestmark = pytest.mark.unit

# Sample test data
INITIAL_SCHEDULE = {
    "active_nightly_builds": ["2.6.2", "2.7.0", "3.0.2", "3.1.1", "3.2.0"],
    "patch_base_versions": ["2.6.1", "3.0.1", "3.1.0"],
    "minor_base_versions": ["2.6.1", "3.1.0"],
}


@pytest.fixture
def mock_github():
    """Setup mock GitHub environment"""
    with patch("nightly_build_helper.Github") as mock_gh:
        # Create mock repo and variable
        mock_repo = Mock()
        mock_var = Mock()
        mock_var.value = json.dumps(INITIAL_SCHEDULE)

        # Setup the chain of mocks
        mock_gh.return_value.get_repo.return_value = mock_repo
        mock_repo.get_variable.return_value = mock_var

        yield {"github": mock_gh, "repo": mock_repo, "variable": mock_var}


@pytest.fixture
def helper(mock_github):
    """Create a NightlyBuildHelper instance with mocked GitHub"""
    with patch.dict("os.environ", {"GH_TOKEN": "fake-token", "GITHUB_REPOSITORY": "fake/repo"}):
        return NightlyBuildHelper()


class TestNightlyBuildHelper:
    def test_initialization(self, helper, mock_github):
        """Test proper initialization of the helper"""
        assert helper.current_schedule == INITIAL_SCHEDULE
        mock_github["repo"].get_variable.assert_called_once_with("NIGHTLY_BUILD_SCHEDULE")

    def test_initialization_missing_env_vars(self):
        """Test initialization fails without required env vars"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GH_TOKEN environment variable is required"):
                NightlyBuildHelper()

    def test_remove_minor_version(self, helper, mock_github):
        """Test removing a minor version (x.y.0)"""
        helper.remove_version("3.2.0")

        # Check that version was removed from active builds
        assert "3.2.0" not in helper.current_schedule["active_nightly_builds"]

        # Check that previous minor base was removed
        assert not any(v.startswith("3.1") for v in helper.current_schedule["minor_base_versions"])

        # Verify save was called
        mock_github["variable"].edit.assert_called_once()

    def test_remove_patch_version(self, helper, mock_github):
        """Test removing a patch version (x.y.z where z > 0)"""
        helper.remove_version("3.0.2")

        # Check that version was removed from active builds
        assert "3.0.2" not in helper.current_schedule["active_nightly_builds"]

        # Check that previous patch base was removed
        assert "3.0.1" not in helper.current_schedule["patch_base_versions"]

        # Verify save was called
        mock_github["variable"].edit.assert_called_once()

    def test_add_next_minor_versions(self, helper, mock_github):
        """Test adding next versions after a minor release"""
        helper.add_next_versions("3.2.0")

        # Check that next patch and minor versions were added
        assert "3.2.1" in helper.current_schedule["active_nightly_builds"]
        assert "3.3.0" in helper.current_schedule["active_nightly_builds"]

        # Check that version was added to base versions
        assert "3.2.0" in helper.current_schedule["patch_base_versions"]
        assert "3.2.0" in helper.current_schedule["minor_base_versions"]

        # Verify save was called
        mock_github["variable"].edit.assert_called_once()

    def test_add_next_patch_versions(self, helper, mock_github):
        """Test adding next versions after a patch release"""
        helper.add_next_versions("3.0.2")

        # Check that next patch version was added
        assert "3.0.3" in helper.current_schedule["active_nightly_builds"]

        # Check that version was added to patch base
        assert "3.0.2" in helper.current_schedule["patch_base_versions"]

        # Verify save was called
        mock_github["variable"].edit.assert_called_once()

    def test_remove_nonexistent_version(self, helper, mock_github):
        """Test removing a version that doesn't exist"""
        helper.remove_version("9.9.9")

        # Check that schedule wasn't modified
        assert helper.current_schedule == INITIAL_SCHEDULE

        # Verify save wasn't called
        mock_github["variable"].edit.assert_not_called()

    def test_version_lists_stay_sorted(self, helper, mock_github):
        """Test that version lists remain sorted after modifications"""
        helper.add_next_versions("3.2.0")

        # Check that lists are sorted
        for list_name in ["active_nightly_builds", "patch_base_versions", "minor_base_versions"]:
            versions = helper.current_schedule[list_name]
            assert versions == sorted(versions, key=lambda x: tuple(map(int, x.split("."))))

    @pytest.mark.parametrize("version", ["invalid", "1.2", "1.2.3.4", "v1.2.3"])
    def test_invalid_version_format(self, helper, version):
        """Test handling of invalid version formats"""
        with pytest.raises(ValueError):
            helper.remove_version(version)
