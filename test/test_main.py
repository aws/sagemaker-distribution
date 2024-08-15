from __future__ import absolute_import

import base64

import pytest

pytestmark = pytest.mark.unit

import os
from unittest.mock import MagicMock, Mock, patch

from config import _image_generator_configs
from main import (
    _get_config_for_image,
    _get_version_tags,
    _push_images_upstream,
    build_images,
    create_and_get_semver_dir,
    create_major_version_artifacts,
    create_minor_version_artifacts,
    create_patch_version_artifacts,
)
from release_notes_generator import (
    _get_image_type_package_metadata,
    _get_package_to_image_type_mapping,
)
from utils import derive_changeset, get_semver


class CreateVersionArgs:
    def __init__(self, runtime_version_upgrade_type, base_patch_version, pre_release_identifier=None, force=False):
        self.base_patch_version = base_patch_version
        self.runtime_version_upgrade_type = runtime_version_upgrade_type
        self.pre_release_identifier = pre_release_identifier
        self.force = force


class BuildImageArgs:
    def __init__(self, target_patch_version, target_ecr_repo=None, force=False):
        self.target_patch_version = target_patch_version
        self.target_ecr_repo = target_ecr_repo
        self.skip_tests = True
        self.force = force


def _create_docker_cpu_env_in_file(file_path, required_package="conda-forge::ipykernel"):
    with open(file_path, "w") as env_in_file:
        env_in_file.write(f"{required_package}\n")


def _create_docker_cpu_env_out_file(
    file_path,
    package_metadata="https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67",
):
    with open(file_path, "w") as env_out_file:
        env_out_file.write(
            f"""# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: linux-64
@EXPLICIT
{package_metadata}\n"""
        )


def _create_docker_gpu_env_in_file(file_path):
    with open(file_path, "w") as env_in_file:
        env_in_file.write("conda-forge::numpy\n")


def _create_additional_packages_gpu_env_in_file(file_path, package_metadata="conda-forge::sagemaker-python-sdk"):
    with open(file_path, "w") as env_in_file:
        env_in_file.write(package_metadata + "\n")


def _create_docker_gpu_env_out_file(file_path):
    with open(file_path, "w") as env_out_file:
        env_out_file.write(
            """# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: linux-64
@EXPLICIT
https://conda.anaconda.org/conda-forge/linux-64/numpy-1.24.2-py38h10c12cc_0.conda#05592c85b9f6931dc2df1e80c0d56294\n"""
        )


def _create_template_docker_file(file_path):
    with open(file_path, "w") as docker_file:
        docker_file.write(
            """ARG TAG_FOR_BASE_MICROMAMBA_IMAGE
        FROM mambaorg / micromamba:$TAG_FOR_BASE_MICROMAMBA_IMAGE\ntemplate_dockerfile\n"""
        )


def _create_prev_docker_file(file_path):
    with open(file_path, "w") as docker_file:
        docker_file.write(
            """ARG TAG_FOR_BASE_MICROMAMBA_IMAGE
        FROM mambaorg / micromamba:$TAG_FOR_BASE_MICROMAMBA_IMAGE\nprevious_dockerfile\n"""
        )


def _create_new_version_artifacts_helper(mocker, tmp_path, version, target_version):
    def mock_get_dir_for_version(base_version):
        pre_release_suffix = "/v" + str(base_version) if base_version.prerelease else ""
        version_string = f"v{base_version.major}.{base_version.minor}.{base_version.patch}" + pre_release_suffix
        # get_dir_for_version returns a str and not PosixPath
        return str(tmp_path) + "/" + version_string

    mocker.patch("main.get_dir_for_version", side_effect=mock_get_dir_for_version)
    input_version = get_semver(version)
    # Create directory for base version
    input_version_dir = create_and_get_semver_dir(input_version)
    print("input_version_dir", input_version_dir)
    # Create env.in and env.out for base version
    _create_docker_cpu_env_in_file(input_version_dir + "/cpu.env.in")
    _create_docker_gpu_env_in_file(input_version_dir + "/gpu.env.in")
    _create_docker_cpu_env_out_file(input_version_dir + "/cpu.env.out")
    _create_docker_gpu_env_out_file(input_version_dir + "/gpu.env.out")
    _create_prev_docker_file(input_version_dir + "/Dockerfile")
    os.makedirs(tmp_path / "template")
    next_version = get_semver(target_version)
    next_major_version = "v" + str(next_version.major)
    os.makedirs(tmp_path / "template" / next_major_version)
    if next_version.major == 1:
        # Create dirs directory under template
        os.makedirs(tmp_path / "template" / next_major_version / "dirs")
    _create_template_docker_file(tmp_path / "template" / next_major_version / "Dockerfile")


def _create_additional_packages_env_in_file_helper(
    mocker, tmp_path, version, include_additional_package=False, use_existing_package_as_additional_package=False
):
    if include_additional_package:

        def mock_get_dir_for_version(base_version):
            pre_release_suffix = "/v" + str(base_version) if base_version.prerelease else ""
            version_string = f"v{base_version.major}.{base_version.minor}.{base_version.patch}" + pre_release_suffix
            # get_dir_for_version returns a str and not PosixPath
            return str(tmp_path) + "/" + version_string

        mocker.patch("main.get_dir_for_version", side_effect=mock_get_dir_for_version)
        input_version = get_semver(version)
        # Create directory for new version
        input_version_dir = create_and_get_semver_dir(input_version)
        additional_env_in_file_path = input_version_dir + "/gpu.additional_packages_env.in"
        if use_existing_package_as_additional_package:
            # Using an older version of numpy.
            _create_additional_packages_gpu_env_in_file(
                additional_env_in_file_path, "conda-forge::numpy[version='>=1.0.4," "<1.1.0']"
            )
        else:
            _create_additional_packages_gpu_env_in_file(additional_env_in_file_path)


def test_get_semver_version():
    # Test invalid version string.
    with pytest.raises(Exception):
        get_semver("1.124.5d")
    # Test version string with build
    with pytest.raises(Exception):
        get_semver("1.124.5+25")
    # Test version string with build and prerelease
    with pytest.raises(Exception):
        get_semver("1.124.5-prerelease+25")
    # Test valid version string.
    assert get_semver("1.124.5") is not None
    assert get_semver("1.124.5-beta") is not None


def test_new_version_artifacts_for_an_input_prerelease_version():
    input_version = "1.23.0-beta"
    args = CreateVersionArgs("patch", input_version, pre_release_identifier="new-beta")
    with pytest.raises(Exception):
        create_patch_version_artifacts(args)
    args = CreateVersionArgs("minor", input_version, pre_release_identifier="new-beta")
    with pytest.raises(Exception):
        create_minor_version_artifacts(args)
    args = CreateVersionArgs("major", input_version, pre_release_identifier="new-beta")
    with pytest.raises(Exception):
        create_major_version_artifacts(args)


@patch("os.path.exists")
@patch("os.path.isdir")
@patch("shutil.rmtree")
@patch("os.makedirs")
@patch("os.listdir")
def test_create_and_get_semver_dir(mock_list_dir, mock_make_dirs, mock_rmtree, mock_path_is_dir, mock_path_exists):
    # case 1: Directory exists and exist_ok is False => Throws Exception
    mock_path_exists.return_value = True
    with pytest.raises(Exception):
        create_and_get_semver_dir(get_semver("1.124.5"))
    # Case 2: Instead of a directory in the path, a file exists.
    mock_path_is_dir.return_value = False
    with pytest.raises(Exception):
        create_and_get_semver_dir(get_semver("1.124.5"), True)
    # Happy case
    mock_path_is_dir.return_value = True
    mock_list_dir.return_value = []
    assert create_and_get_semver_dir(get_semver("1.124.5"), True) is not None


def test_create_new_version_artifacts_for_invalid_upgrade_type():
    input = CreateVersionArgs("test_upgrade", "1.2.3")
    with pytest.raises(Exception):
        create_major_version_artifacts(input)
    with pytest.raises(Exception):
        create_minor_version_artifacts(input)
    with pytest.raises(Exception):
        create_patch_version_artifacts(input)


def _create_and_assert_patch_version_upgrade(
    rel_path,
    mocker,
    tmp_path,
    pre_release_identifier=None,
    include_additional_package=False,
    use_existing_package_as_additional_package=False,
):
    input_version = "0.2.5"
    next_version = get_semver("0.2.6")
    new_version_dir = tmp_path / ("v" + str(next_version))
    base_version_dir = tmp_path / ("v" + input_version)
    if pre_release_identifier:
        new_version_dir = new_version_dir / ("v" + str(next_version) + "-" + pre_release_identifier)
    next_major_version_dir_name = "v" + str(next_version.major)
    if next_version.major == 0:
        rel_path.side_effect = [
            str(base_version_dir / "Dockerfile"),
        ]
    else:
        rel_path.side_effect = [
            str(base_version_dir / "Dockerfile"),
            str(base_version_dir / "dirs"),
        ]
    _create_new_version_artifacts_helper(mocker, tmp_path, input_version, str(next_version))
    _create_additional_packages_env_in_file_helper(
        mocker, tmp_path, str(next_version), include_additional_package, use_existing_package_as_additional_package
    )
    if include_additional_package:
        args = CreateVersionArgs("patch", input_version, pre_release_identifier=pre_release_identifier, force=True)
    else:
        args = CreateVersionArgs("patch", input_version, pre_release_identifier=pre_release_identifier)
    create_patch_version_artifacts(args)
    # Assert new version directory is created

    assert os.path.exists(new_version_dir)
    # Check cpu.env.in and gpu.env.in exists in the new directory
    new_version_dir_files = os.listdir(new_version_dir)
    assert "cpu.env.in" in new_version_dir_files
    assert "gpu.env.in" in new_version_dir_files
    assert "Dockerfile" in new_version_dir_files
    with open(new_version_dir / "Dockerfile", "r") as f:
        assert "previous_dockerfile" in f.read()
    if next_version.major >= 1:
        assert "dirs" in new_version_dir_files
    if include_additional_package:
        assert "gpu.additional_packages_env.in" in new_version_dir_files
    with open(new_version_dir / "cpu.env.in", "r") as f:
        contents = f.read()
        # version of ipykernel in cpu.env.out is 6.21.3
        # so we expect the version string to be >=6.21.3,<6.22.0
        expected_version_string = ">=6.21.3,<6.22.0"
        assert contents.find(expected_version_string) != -1
    with open(new_version_dir / "gpu.env.in", "r") as f:
        contents = f.read()
        # version of numpy in gpu.env.out is 1.24.2
        # so we expect the version string to be >=1.24.2,<1.25.0
        expected_version_string = ">=1.24.2,<1.25.0"
        assert contents.find(expected_version_string) != -1
        if include_additional_package and not use_existing_package_as_additional_package:
            assert contents.find("sagemaker-python-sdk") != -1


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_patch_version_upgrade(rel_path, mocker, tmp_path):
    _create_and_assert_patch_version_upgrade(rel_path, mocker, tmp_path)


@patch("os.path.relpath")
def test_create_new_patch_version_upgrade_with_existing_package_as_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_patch_version_upgrade(
        rel_path, mocker, tmp_path, include_additional_package=True, use_existing_package_as_additional_package=True
    )


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_patch_version_upgrade_with_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_patch_version_upgrade(rel_path, mocker, tmp_path, include_additional_package=True)


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_patch_version_upgrade_with_prerelease(rel_path, mocker, tmp_path):
    _create_and_assert_patch_version_upgrade(rel_path, mocker, tmp_path, "beta")


def _create_and_assert_minor_version_upgrade(
    rel_path,
    mocker,
    tmp_path,
    pre_release_identifier=None,
    include_additional_package=False,
    use_existing_package_as_additional_package=False,
):
    input_version = "1.2.5"
    next_version = get_semver("1.3.0")
    new_version_dir = tmp_path / ("v" + str(next_version))
    if pre_release_identifier:
        new_version_dir = new_version_dir / ("v" + str(next_version) + "-" + pre_release_identifier)
    next_major_version_dir_name = "v" + str(next_version.major)
    if next_version.major == 0:
        rel_path.side_effect = [
            str(tmp_path / "template" / next_major_version_dir_name / "Dockerfile"),
        ]
    else:
        rel_path.side_effect = [
            str(tmp_path / "template" / next_major_version_dir_name / "Dockerfile"),
            str(tmp_path / "template" / next_major_version_dir_name / "dirs"),
        ]
    _create_new_version_artifacts_helper(mocker, tmp_path, input_version, "1.3.0")
    _create_additional_packages_env_in_file_helper(
        mocker, tmp_path, "1.3.0", include_additional_package, use_existing_package_as_additional_package
    )
    if include_additional_package:
        args = CreateVersionArgs("minor", input_version, pre_release_identifier=pre_release_identifier, force=True)
    else:
        args = CreateVersionArgs("minor", input_version, pre_release_identifier=pre_release_identifier)
    create_minor_version_artifacts(args)
    # Assert new version directory is created
    assert os.path.exists(new_version_dir)
    # Check cpu.env.in and gpu.env.in exists in the new directory
    new_version_dir_files = os.listdir(new_version_dir)
    assert "cpu.env.in" in new_version_dir_files
    assert "gpu.env.in" in new_version_dir_files
    assert "Dockerfile" in new_version_dir_files
    with open(new_version_dir / "Dockerfile", "r") as f:
        assert "template_dockerfile" in f.read()
    if next_version.major >= 1:
        assert "dirs" in new_version_dir_files
    if include_additional_package:
        assert "gpu.additional_packages_env.in" in new_version_dir_files
    with open(new_version_dir / "cpu.env.in", "r") as f:
        contents = f.read()
        # version of ipykernel in cpu.env.out is 6.21.3
        # so we expect the version string to be >=6.21.3,<7.0.0
        expected_version_string = ">=6.21.3,<7.0.0"
        assert contents.find(expected_version_string) != -1
    with open(new_version_dir / "gpu.env.in", "r") as f:
        contents = f.read()
        # version of numpy in gpu.env.out is 1.24.2
        # so we expect the version string to be >=1.24.2,<2.0.0
        expected_version_string = ">=1.24.2,<2.0.0"
        assert contents.find(expected_version_string) != -1
        if include_additional_package and not use_existing_package_as_additional_package:
            assert contents.find("sagemaker-python-sdk") != -1


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_minor_version_upgrade(rel_path, mocker, tmp_path):
    _create_and_assert_minor_version_upgrade(rel_path, mocker, tmp_path)


@patch("os.path.relpath")
def test_create_new_minor_version_upgrade_with_existing_package_as_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_minor_version_upgrade(
        rel_path, mocker, tmp_path, include_additional_package=True, use_existing_package_as_additional_package=True
    )


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_minor_version_upgrade_with_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_minor_version_upgrade(rel_path, mocker, tmp_path, include_additional_package=True)


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_minor_version_upgrade_with_prerelease(rel_path, mocker, tmp_path):
    _create_and_assert_minor_version_upgrade(rel_path, mocker, tmp_path, "beta")


def _create_and_assert_major_version_upgrade(
    rel_path,
    mocker,
    tmp_path,
    pre_release_identifier=None,
    include_additional_package=False,
    use_existing_package_as_additional_package=False,
):
    input_version = "0.2.5"
    next_version = get_semver("1.0.0")
    new_version_dir = tmp_path / ("v" + str(next_version))
    if pre_release_identifier:
        new_version_dir = new_version_dir / ("v" + str(next_version) + "-" + pre_release_identifier)
    next_major_version_dir_name = "v" + str(next_version.major)
    if next_version.major == 0:
        rel_path.side_effect = [
            str(tmp_path / "template" / next_major_version_dir_name / "Dockerfile"),
        ]
    else:
        rel_path.side_effect = [
            str(tmp_path / "template" / next_major_version_dir_name / "Dockerfile"),
            str(tmp_path / "template" / next_major_version_dir_name / "dirs"),
        ]
    _create_new_version_artifacts_helper(mocker, tmp_path, input_version, str(next_version))
    _create_additional_packages_env_in_file_helper(
        mocker, tmp_path, str(next_version), include_additional_package, use_existing_package_as_additional_package
    )
    if include_additional_package:
        args = CreateVersionArgs("major", input_version, pre_release_identifier=pre_release_identifier, force=True)
    else:
        args = CreateVersionArgs("major", input_version, pre_release_identifier=pre_release_identifier)
    create_major_version_artifacts(args)
    # Assert new version directory is created
    assert os.path.exists(new_version_dir)
    # Check cpu.env.in and gpu.env.in exists in the new directory
    new_version_dir_files = os.listdir(new_version_dir)
    assert "cpu.env.in" in new_version_dir_files
    assert "gpu.env.in" in new_version_dir_files
    assert "Dockerfile" in new_version_dir_files
    with open(new_version_dir / "Dockerfile", "r") as f:
        assert "template_dockerfile" in f.read()
    if next_version.major >= 1:
        assert "dirs" in new_version_dir_files
    if include_additional_package:
        assert "gpu.additional_packages_env.in" in new_version_dir_files
    with open(new_version_dir / "cpu.env.in", "r") as f:
        contents = f.read()
        # version of ipykernel in cpu.env.out is 6.21.3
        # so we expect the version string to be >=6.21.3,
        expected_version_string = ">=6.21.3'"
        assert contents.find(expected_version_string) != -1
    with open(new_version_dir / "gpu.env.in", "r") as f:
        contents = f.read()
        # version of numpy in gpu.env.out is 1.24.2
        # so we expect the version string to be >=1.24.2,
        expected_version_string = ">=1.24.2'"
        assert contents.find(expected_version_string) != -1
        if include_additional_package and not use_existing_package_as_additional_package:
            assert contents.find("sagemaker-python-sdk") != -1


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_major_version_upgrade(rel_path, mocker, tmp_path):
    _create_and_assert_major_version_upgrade(rel_path, mocker, tmp_path)


@patch("os.path.relpath")
def test_create_new_major_version_upgrade_with_existing_package_as_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_major_version_upgrade(
        rel_path, mocker, tmp_path, include_additional_package=True, use_existing_package_as_additional_package=True
    )


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_major_version_upgrade_with_additional_packages(rel_path, mocker, tmp_path):
    _create_and_assert_major_version_upgrade(rel_path, mocker, tmp_path, include_additional_package=True)


@patch("os.path.relpath")
def test_create_new_version_artifacts_for_major_version_upgrade_with_prerelease(rel_path, mocker, tmp_path):
    _create_and_assert_major_version_upgrade(rel_path, mocker, tmp_path, "beta")


def test_build_images(mocker, tmp_path):
    mock_docker_from_env = MagicMock(name="_docker_client")
    mocker.patch("main._docker_client", new=mock_docker_from_env)
    version = "1.124.5"
    args = BuildImageArgs(version)

    def mock_get_dir_for_version(base_version):
        version_string = f"v{base_version.major}.{base_version.minor}.{base_version.patch}"
        # get_dir_for_version returns a str and not a PosixPath
        return str(tmp_path) + "/" + version_string

    mocker.patch("main.get_dir_for_version", side_effect=mock_get_dir_for_version)
    input_version = get_semver(version)
    # Create directory for base version
    input_version_dir = create_and_get_semver_dir(input_version)
    # Create env.in for base version
    _create_docker_cpu_env_in_file(input_version_dir + "/cpu.env.in")
    _create_docker_cpu_env_in_file(input_version_dir + "/gpu.env.in")
    _create_prev_docker_file(input_version_dir + "/Dockerfile")
    # Assert env.out doesn't exist
    assert os.path.exists(input_version_dir + "/cpu.env.out") is False
    assert os.path.exists(input_version_dir + "/gpu.env.out") is False
    mock_image_1 = Mock()
    mock_image_1.id.return_value = "img1"
    mock_image_2 = Mock()
    mock_image_2.id.return_value = "img2"
    mock_docker_from_env.images.build.side_effect = [(mock_image_1, "logs1"), (mock_image_2, "logs2")]
    mock_docker_from_env.containers.run.side_effect = [
        "container_logs1".encode("utf-8"),
        "container_logs2".encode("utf-8"),
    ]
    # Invoke build images
    build_images(args)
    # Assert env.out exists
    assert os.path.exists(input_version_dir + "/cpu.env.out")
    assert os.path.exists(input_version_dir + "/gpu.env.out")
    # Validate the contents of env.out
    actual_output = set()
    with open(input_version_dir + "/cpu.env.out", "r") as f:
        actual_output.add(f.read())
    with open(input_version_dir + "/gpu.env.out", "r") as f:
        actual_output.add(f.read())
    expected_output = {"container_logs1", "container_logs2"}
    assert actual_output == expected_output


@patch("os.path.exists")
def test_get_version_tags(mock_path_exists):
    version = get_semver("1.124.5")
    file_name = "cpu.env.out"
    # case 1: The given version is the latest for patch, minor and major
    mock_path_exists.side_effect = [False, False, False]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124", "1", "latest"]
    # case 2: The given version is the latest for patch, minor but not major
    # case 2.1 The major version is a prerelease version
    mock_path_exists.side_effect = [False, False, True, False]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124", "1", "latest"]
    # case 2.2 The major version is not a prerelease version
    mock_path_exists.side_effect = [False, False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124", "1"]
    # case 3: The given version is the latest for patch and major but not for minor
    # case 3.1 The minor version is a prerelease version (we need to mock path.exists for major
    # version twice - one for the actual directory, one for the docker file)
    mock_path_exists.side_effect = [False, True, False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124", "1"]
    # case 3.2 The minor version is not a prerelease version
    mock_path_exists.side_effect = [False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124"]
    # case 4: The given version is not the latest for patch, minor, major
    # case 4.1 The patch version is a prerelease version (we need to mock path.exists for minor
    # and major twice - one for the actual directory, one for the docker file)
    mock_path_exists.side_effect = [True, False, True, True, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5", "1.124"]
    # case 4.2 The patch version is not a prerelease version
    mock_path_exists.side_effect = [True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5"]


@patch("os.path.exists")
def test_get_version_tags_with_prerelease_identifier(mock_path_exists):
    version = get_semver("1.124.5-beta")
    file_name = "cpu.env.out"
    # case 1: The given version is the latest for patch, minor and major
    mock_path_exists.side_effect = [False, False, False]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta", "1-beta", "latest-beta"]
    # case 2: The given version is the latest for patch, minor but not major
    # case 2.1 The major version is a different prerelease version
    mock_path_exists.side_effect = [False, False, True, False]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta", "1-beta", "latest-beta"]
    # case 2.2 The major version is not a prerelease version
    mock_path_exists.side_effect = [False, False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta", "1-beta"]
    # case 3: The given version is the latest for patch and major but not for minor
    # case 3.1 The minor version is a prerelease version (we need to mock path.exists for major
    # version twice - one for the actual directory, one for the docker file)
    mock_path_exists.side_effect = [False, True, False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta", "1-beta"]
    # case 3.2 The minor version is not a prerelease version
    mock_path_exists.side_effect = [False, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta"]
    # case 4: The given version is not the latest for patch, minor, major
    # case 4.1 The patch version is a prerelease version (we need to mock path.exists for minor
    # and major twice - one for the actual directory, one for the docker file)
    mock_path_exists.side_effect = [True, False, True, True, True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta", "1.124-beta"]
    # case 4.2 The patch version is not a prerelease version
    mock_path_exists.side_effect = [True, True]
    assert _get_version_tags(version, file_name) == ["1.124.5-beta"]


def _test_push_images_upstream(mocker, repository):
    boto3_client = MagicMock()
    expected_client_name = "ecr-public" if repository.startswith("public.ecr.aws") else "ecr"
    boto3_mocker = mocker.patch("boto3.client", return_value=boto3_client)
    mock_docker_from_env = MagicMock(name="_docker_client")
    mocker.patch("main._docker_client", new=mock_docker_from_env)
    authorization_token_string = "username:password"
    encoded_authorization_token = base64.b64encode(authorization_token_string.encode("ascii"))
    authorization_data = {"authorizationToken": encoded_authorization_token}
    if expected_client_name == "ecr":
        # Private ECR client returns a list of authorizationData.
        authorization_data = [authorization_data]
    boto3_client.get_authorization_token.return_value = {"authorizationData": authorization_data}
    mock_docker_from_env.images.push.side_effect = None
    _push_images_upstream([{"repository": repository, "tag": "0.1"}], "us-west-2")
    assert boto3_mocker.call_args[0][0] == expected_client_name


def test_push_images_upstream_for_private_ecr_repository(mocker):
    repository = "aws_account_id.dkr.ecr.us-west-2.amazonaws.com/my-repository"
    _test_push_images_upstream(mocker, repository)


def test_push_images_upstream_for_public_ecr_repository(mocker):
    repository = "public.ecr.aws/registry_alias/my-repository"
    _test_push_images_upstream(mocker, repository)


@patch("os.path.exists")
def test_get_build_config_for_image(mock_path_exists, tmp_path):
    input_version_dir = str(tmp_path) + "/v2.0.0"
    image_generator_config = _image_generator_configs[2][0]
    # Case 1: Mock os.path.exists to return False
    mock_path_exists.return_value = False
    assert image_generator_config == _get_config_for_image(input_version_dir, image_generator_config, False)
    # Case 2: Mock os.path.exists to return True but force is True
    mock_path_exists.return_value = True
    assert image_generator_config == _get_config_for_image(input_version_dir, image_generator_config, True)
    # Case 3: Mock os.path.exists to return True and force is False
    mock_path_exists.return_value = True
    response = _get_config_for_image(input_version_dir, image_generator_config, False)
    assert response["build_args"]["ENV_IN_FILENAME"] == image_generator_config["env_out_filename"]
    assert "ARG_BASED_ENV_IN_FILENAME" not in response["build_args"]


def test_derive_changeset(tmp_path):
    target_version_dir = str(tmp_path / "v1.0.6")
    source_version_dir = str(tmp_path / "v1.0.5")
    os.makedirs(target_version_dir)
    os.makedirs(source_version_dir)
    # Create env.in of the source version
    _create_docker_cpu_env_in_file(source_version_dir + "/cpu.env.in")
    # Create env.out of the source version
    _create_docker_cpu_env_out_file(
        source_version_dir + "/cpu.env.out",
        package_metadata="https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#8c1f6bf32a6ca81232c4853d4165ca67",
    )
    # Create env.in of the target version, which has additional dependency on boto3
    target_env_in_packages = "conda-forge::ipykernel\nconda-forge::boto3"
    _create_docker_cpu_env_in_file(target_version_dir + "/cpu.env.in", required_package=target_env_in_packages)
    target_env_out_packages = (
        "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.6-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67\n"
        "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#8c1f6bf32a6ca81232c4853d4165ca67"
    )
    _create_docker_cpu_env_out_file(target_version_dir + "/cpu.env.out", package_metadata=target_env_out_packages)
    expected_upgrades = {"ipykernel": ["6.21.3", "6.21.6"]}
    expected_new_packages = {"boto3": "1.2"}
    actual_upgrades, actual_new_packages = derive_changeset(
        target_version_dir, source_version_dir, _image_generator_configs[1][1]
    )
    assert expected_upgrades == actual_upgrades
    assert expected_new_packages == actual_new_packages


def test_generate_release_notes(tmp_path):
    target_version_dir = str(tmp_path / "v1.0.6")
    target_version = get_semver("1.0.6")
    os.makedirs(target_version_dir)
    # Create env.in of the target version, which has additional dependency on boto3
    target_env_in_packages = "conda-forge::ipykernel\nconda-forge::boto3"
    _create_docker_cpu_env_in_file(target_version_dir + "/cpu.env.in", required_package=target_env_in_packages)
    target_env_out_packages = (
        "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.6-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67\n"
        "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.23.4"
        "-cuda112py38hd_0.conda#8c1f6bf32a6ca81232c4853d4165ca67"
    )
    _create_docker_cpu_env_out_file(target_version_dir + "/cpu.env.out", package_metadata=target_env_out_packages)
    # GPU contains only numpy
    _create_docker_gpu_env_in_file(target_version_dir + "/gpu.env.in")
    _create_docker_gpu_env_out_file(target_version_dir + "/gpu.env.out")
    # Verify _get_image_type_package_metadata
    image_type_package_metadata = _get_image_type_package_metadata(target_version_dir, target_version)
    assert len(image_type_package_metadata) == 2
    assert image_type_package_metadata["gpu"] == {"numpy": "1.24.2"}
    assert image_type_package_metadata["cpu"] == {"ipykernel": "6.21.6", "boto3": "1.23.4"}
    # Verify _get_package_to_image_type_mapping
    package_to_image_type_mapping = _get_package_to_image_type_mapping(image_type_package_metadata)
    assert len(package_to_image_type_mapping) == 3
    assert package_to_image_type_mapping["numpy"] == {"gpu": "1.24.2"}
    assert package_to_image_type_mapping["ipykernel"] == {"cpu": "6.21.6"}
    assert package_to_image_type_mapping["boto3"] == {"cpu": "1.23.4"}
