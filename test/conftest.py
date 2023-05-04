import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--local-image-id", help="Id of a locally available Docker image against which the tests should run."
    )
    parser.addoption(
        "--use-gpu", action='store_true', help="Boolean on whether to use GPUs or not"
    )


@pytest.fixture
def local_image_id(request) -> str:
    return request.config.getoption("--local-image-id")


@pytest.fixture
def use_gpu(request) -> bool:
    return request.config.getoption("--use-gpu")
