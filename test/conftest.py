import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--local-image-version",
        help="Version of a locally available SageMaker Distribution "
        "Docker image against which the tests should run. Note: "
        "We expect the local docker image to have "
        "'localhost/sagemaker-distribution' as the repository and "
        "'<version>-{cpu/gpu}' as the tag",
    )
    parser.addoption("--use-gpu", action="store_true", help="Boolean on whether to use GPUs or not")


@pytest.fixture
def local_image_version(request) -> str:
    return request.config.getoption("--local-image-version")


@pytest.fixture
def use_gpu(request) -> bool:
    return request.config.getoption("--use-gpu")


# Add the github workflows utils directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir / ".github" / "workflows" / "utils"))
