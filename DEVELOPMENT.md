## Local development

This project uses Conda to manage its dependencies. Run the following to setup your local environment:

```shell
conda env update --file environment.lock -n sagemaker-distribution
```

## Tests

### Tests against an Amazon SageMaker Distribution image

The [test_dockerfile_based_harness.py](test/test_dockerfile_based_harness.py) contains test cases that can be run
against an Amazon SageMaker Distribution image: this could be a pre-built image from our ECR repository, or it could be
an image that you built locally using the `build` command:

```shell
python ./src/main.py build --target-patch-version x.y.z
```

Run the following to invoke those tests:

```shell
pytest --local-image-id REPLACE_ME_WITH_IMAGE_ID
```

## Code Style

Install pre-commit to run code style checks before each commit:

```shell
pre-commit install
```

To run formatters for all existing files, use:

```shell
pre-commit run --all-files
```

pre-commit checks can be disabled for a particular commit with git commit -n.

You can also pass a `--use-gpu` flag if the test machine has Nvidia GPU(s) and necessary Nvidia drivers.

### Unit tests for the project's source code

TODO.
