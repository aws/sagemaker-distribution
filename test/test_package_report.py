from __future__ import absolute_import

import pytest

pytestmark = pytest.mark.unit

from unittest.mock import patch

from config import _image_generator_configs
from package_report import (
    _generate_python_package_dependency_report,
    _generate_python_package_size_report_per_image,
    _get_installed_package_versions_and_conda_versions,
)
from utils import get_match_specs, get_semver


def _create_env_in_docker_file(file_path):
    with open(file_path, "w") as env_in_file:
        env_in_file.write(
            f"""# This file is auto-generated.
conda-forge::ipykernel
conda-forge::numpy[version=\'>=1.0.17,<2.0.0\']"""
        )


def _create_target_env_in_docker_file(file_path):
    with open(file_path, "w") as env_in_file:
        env_in_file.write(
            f"""# This file is auto-generated.
conda-forge::ipykernel
conda-forge::numpy[version=\'>=1.0.17,<2.0.0\']
conda-forge::sagemaker-headless-execution-driver[version='>=0.0.12,<0.1.0']
"""
        )


def _create_env_out_docker_file(
    file_path,
    package_metadata="""https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67
    https://conda.anaconda.org/conda-forge/linux-64/numpy-1.24.2-py38h10c12cc_0.conda#05592c85b9f6931dc2df1e80c0d56294""",
):
    with open(file_path, "w") as env_out_file:
        env_out_file.write(
            f"""# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: linux-64
@EXPLICIT
{package_metadata}\n"""
        )


def _create_base_image_package_metadata():
    return {
        "libllvm18": {"version": "18.1.1", "size": 37301754},
        "python": {"version": "3.12.1", "size": 30213651},
        "tqdm": {"version": "4.66.2", "size": 89567},
    }


def _create_target_image_package_metadata():
    return {
        "libllvm18": {"version": "18.1.2", "size": 38407510},
        "python": {"version": "3.12.2", "size": 32312631},
        "libclang": {"version": "18.1.2", "size": 19272925},
        "tqdm": {"version": "4.66.2", "size": 89567},
    }


def test_get_match_specs(tmp_path):
    env_out_file_path = tmp_path / "env.out"
    _create_env_out_docker_file(env_out_file_path)
    match_spec_out = get_match_specs(env_out_file_path)
    ipykernel_match_spec = match_spec_out["ipykernel"]
    assert str(ipykernel_match_spec.get("version")).removeprefix("==") == "6.21.3"
    numpy_match_spec = match_spec_out["numpy"]
    assert str(numpy_match_spec.get("version")).removeprefix("==") == "1.24.2"
    assert ipykernel_match_spec.get("subdir") == "noarch"
    assert numpy_match_spec.get("subdir") == "linux-64"
    assert len(match_spec_out) == 3
    # Test bad file path
    env_out_file_path = tmp_path / "bad.env.out"
    match_spec_out = get_match_specs(env_out_file_path)
    assert len(match_spec_out) == 0


@patch("conda.cli.python_api.run_command")
def test_get_installed_package_versions_and_conda_versions(mock_run_command, tmp_path):
    mock_run_command.return_value = (
        '{"ipykernel":[{"version": "6.21.3"}], "numpy":[{"version": '
        '"1.24.3"},{"version":"1.26.0"},{"version":"2.1.0"}]}',
        "",
        0,
    )
    env_in_file_path = tmp_path / "cpu.env.in"
    _create_env_in_docker_file(env_in_file_path)
    env_out_file_path = tmp_path / "cpu.env.out"
    _create_env_out_docker_file(env_out_file_path)
    # Validate results for patch version release
    # _image_generator_configs[0][1] is for v0 CPU
    match_spec_out, latest_package_versions_in_conda_forge = _get_installed_package_versions_and_conda_versions(
        _image_generator_configs[0][1], str(tmp_path), get_semver("0.4.2")
    )
    ipykernel_match_spec = match_spec_out["ipykernel"]
    assert str(ipykernel_match_spec.get("version")).removeprefix("==") == "6.21.3"
    numpy_match_spec = match_spec_out["numpy"]
    assert str(numpy_match_spec.get("version")).removeprefix("==") == "1.24.2"
    assert latest_package_versions_in_conda_forge["ipykernel"] == "6.21.3"
    assert latest_package_versions_in_conda_forge["numpy"] == "1.24.3"
    # Validate results for minor version release
    match_spec_out, latest_package_versions_in_conda_forge = _get_installed_package_versions_and_conda_versions(
        _image_generator_configs[0][1], str(tmp_path), get_semver("0.5.0")
    )
    ipykernel_match_spec = match_spec_out["ipykernel"]
    assert str(ipykernel_match_spec.get("version")).removeprefix("==") == "6.21.3"
    numpy_match_spec = match_spec_out["numpy"]
    assert str(numpy_match_spec.get("version")).removeprefix("==") == "1.24.2"
    assert latest_package_versions_in_conda_forge["ipykernel"] == "6.21.3"
    # Only for numpy there is a new minor version available.
    assert latest_package_versions_in_conda_forge["numpy"] == "1.26.0"
    # Validate results for major version release
    match_spec_out, latest_package_versions_in_conda_forge = _get_installed_package_versions_and_conda_versions(
        _image_generator_configs[1][1], str(tmp_path), get_semver("1.0.0")
    )
    ipykernel_match_spec = match_spec_out["ipykernel"]
    assert str(ipykernel_match_spec.get("version")).removeprefix("==") == "6.21.3"
    numpy_match_spec = match_spec_out["numpy"]
    assert str(numpy_match_spec.get("version")).removeprefix("==") == "1.24.2"
    assert latest_package_versions_in_conda_forge["ipykernel"] == "6.21.3"
    # Only for numpy there is a new major version available.
    assert latest_package_versions_in_conda_forge["numpy"] == "2.1.0"


def test_generate_package_size_report(capsys):
    base_pkg_metadata = _create_base_image_package_metadata()
    target_pkg_metadata = _create_target_image_package_metadata()

    _generate_python_package_size_report_per_image(
        base_pkg_metadata, target_pkg_metadata, _image_generator_configs[1][1], "1.6.1", "1.6.2"
    )

    captured = capsys.readouterr()
    # Assert total size delta report
    assert "85.91MB|64.47MB|21.44MB|33.25" in captured.out

    # Assert size delta report for each changed package
    assert "libclang|18.1.2|-|18.38MB|-" in captured.out
    assert "python|3.12.2|3.12.1|2.00MB|6.95" in captured.out
    assert "libllvm18|18.1.2|18.1.1|1.05MB|2.96" in captured.out
    assert "tqdm|4.66.2|4.66.2" not in captured.out

    # Assert top-k largest package report
    assert "libllvm18|18.1.2|36.63MB" in captured.out
    assert "python|3.12.2|30.82MB" in captured.out
    assert "libclang|18.1.2|18.38MB" in captured.out
    assert "tqdm|4.66.2|87.47KB" in captured.out

    # Assert size validation message
    assert (
        "The total size of newly introduced Python packages is 18.38MB, accounts for ${\color{red}21.39}$% of the total package size."
        in captured.out
    )


def test_generate_package_size_report_when_base_version_is_not_present(capsys):
    target_pkg_metadata = _create_target_image_package_metadata()

    _generate_python_package_size_report_per_image(
        None, target_pkg_metadata, _image_generator_configs[1][1], None, "1.6.2"
    )

    captured = capsys.readouterr()
    # Assert total size delta report
    assert (
        "WARNING: No Python package metadata file found for base image, only partial results will be shown."
        in captured.out
    )
    assert "85.91MB|-|-|-" in captured.out

    # Assert top-k largest package report
    assert "libllvm18|18.1.2|36.63MB" in captured.out
    assert "python|3.12.2|30.82MB" in captured.out
    assert "libclang|18.1.2|18.38MB" in captured.out
    assert "tqdm|4.66.2|87.47KB" in captured.out


@patch("conda.cli.python_api.run_command")
def test_generate_package_dependency_report(mock_conda_command, tmp_path, capsys):
    base_version_dir = tmp_path / "base"
    base_version_dir.mkdir()

    target_version_dir = tmp_path / "target"
    target_version_dir.mkdir()
    _create_target_env_in_docker_file(target_version_dir / "cpu.env.in")

    _create_env_out_docker_file(
        str(base_version_dir) + "/cpu.env.out",
        package_metadata="""https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#8c1f6bf32a6ca81232c4853d4165ca67
        https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#8c1f6bf32a6ca81232c4853d4165ca67""",
    )

    target_env_out_packages = (
        "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.6-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67\n"
        "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#8c1f6bf32a6ca81232c4853d4165ca67\n"
        "https://conda.anaconda.org/conda-forge/noarch/sagemaker-headless-execution-driver-0.0.13-pyhd8ed1ab_0.conda#feaec93c21652caac71ed7ecf450cb17"
    )
    _create_env_out_docker_file(str(target_version_dir) + "/cpu.env.out", package_metadata=target_env_out_packages)

    mock_conda_command.return_value = (
        '{"sagemaker-headless-execution-driver":[{"version":"0.0.13","depends":["nbconvert","papermill >=2.4","python >3.8"]}]}',
        "",
        0,
    )

    _generate_python_package_dependency_report(
        _image_generator_configs[1][1], str(base_version_dir), str(target_version_dir)
    )

    captured = capsys.readouterr()
    # Assert dependency report for newly added packages
    assert "sagemaker-headless-execution-driver|0.0.13|['nbconvert', 'papermill >=2.4', 'python >3.8']" in captured.out

    # Assert existing packages not in report
    assert "ipykernel" not in captured.out
    assert "numpy" not in captured.out
