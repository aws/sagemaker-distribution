import subprocess

import docker
import pytest


_docker_client = docker.from_env()


@pytest.mark.parametrize("dockerfile_path", ["pandas.test.Dockerfile",
                                             "pytorch.examples.Dockerfile",
                                             "tensorflow.examples.Dockerfile"])
def test_dockerfiles(dockerfile_path: str, local_image_id: str, use_gpu: bool):
    print(f'Will start running test for: {dockerfile_path} against: {local_image_id}')
    image, _ = _docker_client.images.build(path='test/test_artifacts', dockerfile=dockerfile_path,
                                           rm=True, buildargs={'COSMOS_IMAGE': local_image_id})
    print(f'Built a test image: {image.id}, will now execute its default CMD.')
    # Execute the new image once. Mark the current test successful/failed based on container's exit code. (We assume
    # that the image would have supplied the right entrypoint.

    device_requests = []
    if use_gpu and is_nvidia_drivers_available():
        # Pass all available GPUs, if available.
        device_requests.append(docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]))

    # We assume that the image above would have supplied the right entrypoint, so we just run it as is. If the container
    # didn't execute successfully, the Docker client below will throw an error and fail the test.
    # A consequence of this design decision is that any test assertions should go inside the container's entry-point.
    _docker_client.containers.run(image=image.id, detach=False, auto_remove=True, device_requests=device_requests)


# The following is a simple function to check whether the local machine has at least 1 GPU and some Nvidia driver
# version.
def is_nvidia_drivers_available() -> bool:
    exitcode, output = subprocess.getstatusoutput("nvidia-smi --query-gpu=driver_version --format=csv,noheader --id=0")
    if exitcode == 0:
        print(f'Found Nvidia driver version: {output}')
    else:
        print(f'No Nvidia drivers found on the machine. Error output: {output}')

    return exitcode == 0
