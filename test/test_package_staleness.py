from __future__ import absolute_import

from conda.cli.python_api import run_command
import pytest

pytestmark = pytest.mark.unit

from utils import get_semver, get_match_specs
from package_staleness import _get_installed_package_versions_and_conda_versions
from config import _image_generator_configs
from unittest.mock import patch, Mock, MagicMock


def _create_env_in_docker_file(file_path):
    with open(file_path, 'w') as env_in_file:
        env_in_file.write(f'''# This file is auto-generated.
conda-forge::ipykernel
conda-forge::numpy[version=\'>=1.0.17,<2.0.0\']''')


def _create_env_out_docker_file(file_path):
    with open(file_path, 'w') as env_out_file:
        env_out_file.write(f'''# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: linux-64
https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#8c1f6bf32a6ca81232c4853d4165ca67
https://conda.anaconda.org/conda-forge/linux-64/numpy-1.24.2-py38h10c12cc_0.conda#05592c85b9f6931dc2df1e80c0d56294\n''')


def test_get_match_specs(tmp_path):
    env_out_file_path = tmp_path / 'env.out'
    _create_env_out_docker_file(env_out_file_path)
    match_spec_out = get_match_specs(env_out_file_path)
    ipykernel_match_spec = match_spec_out['ipykernel']
    assert str(ipykernel_match_spec.get('version')).removeprefix('==') == '6.21.3'
    numpy_match_spec = match_spec_out['numpy']
    assert str(numpy_match_spec.get('version')).removeprefix('==') == '1.24.2'
    assert ipykernel_match_spec.get('subdir') == 'noarch'
    assert numpy_match_spec.get('subdir') == 'linux-64'
    assert len(match_spec_out) == 2
    # Test bad file path
    env_out_file_path = tmp_path / 'bad.env.out'
    match_spec_out = get_match_specs(env_out_file_path)
    assert len(match_spec_out) == 0


@patch("conda.cli.python_api.run_command")
def test_get_installed_package_versions_and_conda_versions(mock_run_command, tmp_path):
    mock_run_command.return_value = ('{"ipykernel":[{"version": "6.21.3"}], "numpy":[{"version": '
                                     '"1.24.3"},{"version":"1.26.0"},{"version":"2.1.0"}]}', '', 0)
    env_in_file_path = tmp_path / 'cpu.env.in'
    _create_env_in_docker_file(env_in_file_path)
    env_out_file_path = tmp_path / 'cpu.env.out'
    _create_env_out_docker_file(env_out_file_path)
    # Validate results for patch version release
    # _image_generator_configs[1] is for CPU
    match_spec_out, latest_package_versions_in_conda_forge = \
        _get_installed_package_versions_and_conda_versions(_image_generator_configs[1],
                                                           str(tmp_path), get_semver('0.4.2'))
    ipykernel_match_spec = match_spec_out['ipykernel']
    assert str(ipykernel_match_spec.get('version')).removeprefix('==') == '6.21.3'
    numpy_match_spec = match_spec_out['numpy']
    assert str(numpy_match_spec.get('version')).removeprefix('==') == '1.24.2'
    assert latest_package_versions_in_conda_forge['ipykernel'] == '6.21.3'
    assert latest_package_versions_in_conda_forge['numpy'] == '1.24.3'
    # Validate results for minor version release
    match_spec_out, latest_package_versions_in_conda_forge = \
        _get_installed_package_versions_and_conda_versions(_image_generator_configs[1],
                                                           str(tmp_path), get_semver('0.5.0'))
    ipykernel_match_spec = match_spec_out['ipykernel']
    assert str(ipykernel_match_spec.get('version')).removeprefix('==') == '6.21.3'
    numpy_match_spec = match_spec_out['numpy']
    assert str(numpy_match_spec.get('version')).removeprefix('==') == '1.24.2'
    assert latest_package_versions_in_conda_forge['ipykernel'] == '6.21.3'
    # Only for numpy there is a new minor version available.
    assert latest_package_versions_in_conda_forge['numpy'] == '1.26.0'
    # Validate results for major version release
    match_spec_out, latest_package_versions_in_conda_forge = \
        _get_installed_package_versions_and_conda_versions(_image_generator_configs[1],
                                                           str(tmp_path), get_semver('1.0.0'))
    ipykernel_match_spec = match_spec_out['ipykernel']
    assert str(ipykernel_match_spec.get('version')).removeprefix('==') == '6.21.3'
    numpy_match_spec = match_spec_out['numpy']
    assert str(numpy_match_spec.get('version')).removeprefix('==') == '1.24.2'
    assert latest_package_versions_in_conda_forge['ipykernel'] == '6.21.3'
    # Only for numpy there is a new major version available.
    assert latest_package_versions_in_conda_forge['numpy'] == '2.1.0'
