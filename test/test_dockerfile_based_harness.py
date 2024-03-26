import subprocess
import os
import docker
import pytest
from config import _image_generator_configs
from docker.errors import BuildError
from semver import Version
from typing import List
from utils import (
    get_dir_for_version,
    get_semver,
    get_match_specs,
)

_docker_client = docker.from_env()


@pytest.mark.cpu
@pytest.mark.parametrize("dockerfile_path, required_packages", [
    ("keras.test.Dockerfile", ['keras']),
    ("autogluon.test.Dockerfile", ['autogluon']),
    ("matplotlib.test.Dockerfile", ['matplotlib']),
    ("sagemaker-headless-execution-driver.test.Dockerfile", ['sagemaker-headless-execution-driver']),
    ("scipy.test.Dockerfile", ['scipy']),
    ("numpy.test.Dockerfile", ['numpy']),
    ("boto3.test.Dockerfile", ['boto3']),
    ("pandas.test.Dockerfile", ['pandas']),
    ("sm-python-sdk.test.Dockerfile", ['sagemaker-python-sdk']),
    ("pytorch.examples.Dockerfile", ['pytorch']),
    ("tensorflow.examples.Dockerfile", ['tensorflow']),
    ("jupyter-ai.test.Dockerfile", ['jupyter-ai']),
    ("jupyter-dash.test.Dockerfile", ['jupyter-dash']),
    ("jupyterlab-lsp.test.Dockerfile", ['jupyterlab-lsp']),
    ("jupyter-lsp-server.test.Dockerfile", ['jupyter-lsp-server']),
    ("notebook.test.Dockerfile", ['notebook']),
    ("glue-sessions.test.Dockerfile", ['aws-glue-sessions']),
    ("altair.test.Dockerfile", ['altair']),
    ("sagemaker-studio-analytics-extension.test.Dockerfile", ['sagemaker-studio-analytics-extension']),
    ("amazon-codewhisperer-jupyterlab-ext.test.Dockerfile", ['amazon-codewhisperer-jupyterlab-ext']),
    ("jupyterlab-git.test.Dockerfile", ['jupyterlab-git']),
    ("maxdome_jupyter_server_extension.test.Dockerfile", ['maxdome_jupyter_server_extension']),
    ("maxdome_jupyter_session_manager.test.Dockerfile", ['maxdome_jupyter_session_manager']),
    ("maxdome_toolkit_cli.test.Dockerfile",['maxdome_toolkit_cli']),
    ("serve.test.Dockerfile", ['serve-langchain'])])
def test_dockerfiles_for_cpu(dockerfile_path: str, required_packages: List[str],
                             local_image_version: str, use_gpu: bool):
    _validate_docker_images(dockerfile_path, required_packages, local_image_version, use_gpu, 'cpu')


@pytest.mark.gpu
@pytest.mark.parametrize("dockerfile_path, required_packages", [
    ("keras.test.Dockerfile", ['keras']),
    ("autogluon.test.Dockerfile", ['autogluon']),
    ("matplotlib.test.Dockerfile", ['matplotlib']),
    ("sagemaker-headless-execution-driver.test.Dockerfile", ['sagemaker-headless-execution-driver']),
    ("scipy.test.Dockerfile", ['scipy']),
    ("numpy.test.Dockerfile", ['numpy']),
    ("boto3.test.Dockerfile", ['boto3']),
    ("pandas.test.Dockerfile", ['pandas']),
    ("sm-python-sdk.test.Dockerfile", ['sagemaker-python-sdk']),
    ("pytorch.examples.Dockerfile", ['pytorch']),
    ("tensorflow.examples.Dockerfile", ['tensorflow']),
    ("glue-sessions.test.Dockerfile", ['aws-glue-sessions']),
    ("jupyter-ai.test.Dockerfile", ['jupyter-ai']),
    ("jupyter-dash.test.Dockerfile", ['jupyter-dash']),
    ("jupyterlab-lsp.test.Dockerfile", ['jupyterlab-lsp']),
    ("jupyter-lsp-server.test.Dockerfile", ['jupyter-lsp-server']),
    ("notebook.test.Dockerfile", ['notebook']),
    ("glue-sessions.test.Dockerfile", ['aws-glue-sessions']),
    ("altair.test.Dockerfile", ['altair']),
    ("sagemaker-studio-analytics-extension.test.Dockerfile", ['sagemaker-studio-analytics-extension']),
    ("amazon-codewhisperer-jupyterlab-ext.test.Dockerfile", ['amazon-codewhisperer-jupyterlab-ext']),
    ("jupyterlab-git.test.Dockerfile", ['jupyterlab-git']),
    ("maxdome_jupyter_server_extension.test.Dockerfile", ['maxdome_jupyter_server_extension']),
    ("maxdome_jupyter_session_manager.test.Dockerfile", ['maxdome_jupyter_session_manager']),
    ("maxdome_toolkit_cli.test.Dockerfile",['maxdome_toolkit_cli']),
    ("serve.test.Dockerfile", ['serve-langchain'])])
def test_dockerfiles_for_gpu(dockerfile_path: str, required_packages: List[str],
                             local_image_version: str, use_gpu: bool):
    _validate_docker_images(dockerfile_path, required_packages, local_image_version, use_gpu, 'gpu')



# The following is a simple function to check whether the local machine has at least 1 GPU and some Nvidia driver
# version.
def _is_nvidia_drivers_available() -> bool:
    exitcode, output = subprocess.getstatusoutput("nvidia-smi --query-gpu=driver_version --format=csv,noheader --id=0")
    if exitcode == 0:
        print(f'Found Nvidia driver version: {output}')
    else:
        print(f'No Nvidia drivers found on the machine. Error output: {output}')

    return exitcode == 0


def _check_docker_file_existence(dockerfile_name: str, test_artifacts_path: str):
    if not os.path.exists(f'{test_artifacts_path}/{dockerfile_name}'):
        pytest.skip(f'Skipping test because {dockerfile_name} does not exist.')


def _check_required_package_constraints(target_version: Version, required_packages: List[str],
                                        image_type: str):
    target_version_dir = get_dir_for_version(target_version)
    if not os.path.exists(target_version_dir):
        pytest.skip(f'Skipping test because {target_version_dir} does not exist.')
    # fetch the env.out file for this image_type
    env_out_file_name = next(config['env_out_filename'] for config in _image_generator_configs if
                             config['image_type'] == image_type)
    env_out_path = f'{target_version_dir}/{env_out_file_name}'
    if not os.path.exists(env_out_path):
        pytest.skip(f'Skipping test because {env_out_path} does not exist.')
    target_match_spec_out = get_match_specs(env_out_path)
    for required_package in required_packages:
        if required_package not in target_match_spec_out:
            pytest.skip(f'Skipping test because {required_package} is not present in {env_out_file_name}')


def _validate_docker_images(dockerfile_path: str, required_packages: List[str],
                            local_image_version: str, use_gpu: bool, image_type: str):
    target_version = get_semver(local_image_version)
    test_artifacts_path = f'test/test_artifacts/v{str(target_version.major)}'
    _check_docker_file_existence(dockerfile_path, test_artifacts_path)
    _check_required_package_constraints(target_version, required_packages, image_type)
    image_tag_generator_from_config = next(config['image_tag_generator'] for config in
                                           _image_generator_configs if config['image_type'] ==
                                           image_type)
    docker_image_tag = image_tag_generator_from_config.format(image_version=local_image_version)
    docker_image_identifier = f'localhost/sagemaker-distribution:{docker_image_tag}'
    print(f'Will start running test for: {dockerfile_path} against: {docker_image_identifier}')

    try:
        image, _ = _docker_client.images.build(path=test_artifacts_path,
                                               dockerfile=dockerfile_path,
                                               tag=dockerfile_path.lower().replace('.', '-'),
                                               rm=True, buildargs={'COSMOS_IMAGE': docker_image_identifier})
    except BuildError as e:
        for line in e.build_log:
            if 'stream' in line:
                print(line['stream'].strip())
        # After printing the logs raise the exception (which is the old behavior)
        raise
    print(f'Built a test image: {image.id}, will now execute its default CMD.')
    # Execute the new image once. Mark the current test successful/failed based on container's exit code. (We assume
    # that the image would have supplied the right entrypoint.

    device_requests = []
    if use_gpu and _is_nvidia_drivers_available():
        # Pass all available GPUs, if available.
        device_requests.append(docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]))

    # We assume that the image above would have supplied the right entrypoint, so we just run it as is. If the container
    # didn't execute successfully, the Docker client below will throw an error and fail the test.
    # A consequence of this design decision is that any test assertions should go inside the container's entry-point.

    container = _docker_client.containers.run(image=image.id, detach=True, stderr=True,
                                      device_requests=device_requests)
    # Wait till container completes execution
    result = container.wait()
    exit_code = result["StatusCode"]
    if exit_code != 0:
        # Print STD out only during test failure
        print(container.logs().decode('utf-8'))
    # Remove the container.
    container.remove(force=True)
    _docker_client.images.remove(image=image.id, force=True)
    # Fail the test if docker exit code is not zero
    assert exit_code == 0
