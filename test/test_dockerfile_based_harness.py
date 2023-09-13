import subprocess

import docker
import pytest
from docker.errors import BuildError

_docker_client = docker.from_env()


@pytest.mark.cpu
@pytest.mark.parametrize("dockerfile_path", ["keras.test.Dockerfile",
                                             "matplotlib.test.Dockerfile",
                                             "scipy.test.Dockerfile",
                                             "numpy.test.Dockerfile",
                                             "boto3.test.Dockerfile",
                                             "pandas.test.Dockerfile",
                                             "sm-python-sdk.test.Dockerfile",
                                             "pytorch.examples.Dockerfile",
                                             "tensorflow.examples.Dockerfile"])
def test_dockerfiles_for_cpu(dockerfile_path: str, local_image_id: str, use_gpu: bool):
    _validate_docker_images(dockerfile_path, local_image_id, use_gpu)


@pytest.mark.gpu
@pytest.mark.parametrize("dockerfile_path", ["keras.test.Dockerfile",
                                             "matplotlib.test.Dockerfile",
                                             "scipy.test.Dockerfile",
                                             "numpy.test.Dockerfile",
                                             "boto3.test.Dockerfile",
                                             "pandas.test.Dockerfile",
                                             "sm-python-sdk.test.Dockerfile",
                                             "pytorch.examples.Dockerfile",
                                             "tensorflow.examples.Dockerfile"])
def test_dockerfiles_for_gpu(dockerfile_path: str, local_image_id: str, use_gpu: bool):
    _validate_docker_images(dockerfile_path, local_image_id, use_gpu)



# The following is a simple function to check whether the local machine has at least 1 GPU and some Nvidia driver
# version.
def _is_nvidia_drivers_available() -> bool:
    exitcode, output = subprocess.getstatusoutput("nvidia-smi --query-gpu=driver_version --format=csv,noheader --id=0")
    if exitcode == 0:
        print(f'Found Nvidia driver version: {output}')
    else:
        print(f'No Nvidia drivers found on the machine. Error output: {output}')

    return exitcode == 0


def _validate_docker_images(dockerfile_path: str, local_image_id: str, use_gpu: bool):
    print(f'Will start running test for: {dockerfile_path} against: {local_image_id}')
    try:
        image, _ = _docker_client.images.build(path='test/test_artifacts',
                                               dockerfile=dockerfile_path,
                                               rm=True, buildargs={'COSMOS_IMAGE': local_image_id})
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
    # Remove the test docker image after running the test. Don't remove any untagged parent image.
    _docker_client.images.remove(image=image.id, force=True, noprune=True)
    # Fail the test if docker exit code is not zero
    assert exit_code == 0
