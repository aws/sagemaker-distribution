#!/bin/bash

# The Dockerfile sets AWS_DEFAULT_REGION=us-east-1, which the SDK's unit tests require.

# We need to checkout the version of sagemaker-python-sdk that is installed in the mamba environment.
pysdk_version=$(micromamba list | awk '$1=="sagemaker-python-sdk" {print $2}')

# Checkout the corresponding sagemaker-python-sdk version
git checkout tags/v$pysdk_version

# SDK v3 is a monorepo (sagemaker-core, -train, -serve, -mlops). The installed sub-packages are released on their
# own versions, so only sagemaker-core's unit tests reliably match the installed code at the v3 tag.
# tests/unit/local needs a local Docker/SageMaker-local setup; test_version.py reads a VERSION file from the source tree.
cd sagemaker-core
pytest tests/unit -n auto -p no:cacheprovider \
    --ignore tests/unit/local \
    --ignore tests/unit/modules/local_core \
    --ignore tests/unit/test_version.py || exit $?
