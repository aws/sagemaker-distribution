#!/bin/bash

# We need to checkout the version of sagemaker-python-sdk that is installed in the mamba environment.

# Sagemaker Python SDK's unit tests requires AWS_DEFAULT_REGION to be set. So, using an arbitrary value of us-east-1
export AWS_DEFAULT_REGION=us-west-2

pysdk_version=$(micromamba list | grep sagemaker-python-sdk | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding sagemaker-python-sdk version
git checkout tags/v$pysdk_version

# Install test dependencies of sagemaker-python-sdk
# Using pip as some of the packages are not available on conda-forge
pip install -r requirements/extras/test_requirements.txt

# Run the unit tests, ignoring tests which require AWS Configuration
# TODO: Re-evaluate the ignored tests since we are setting the AWS_DEFAULT_REGION as part of the Dockerfile.
pytest tests/unit --ignore=tests/unit/sagemaker/feature_store/ --ignore=tests/unit/sagemaker/jumpstart/ --ignore=tests/unit/sagemaker/workflow/ \
    --ignore=tests/unit/sagemaker/async_inference --ignore=tests/unit/test_model_card.py --ignore=tests/unit/test_model_card.py --ignore=tests/unit/test_processing.py \
    --ignore=tests/unit/test_tensorboard.py --ignore=tests/unit/sagemaker/async_inference --ignore=tests/unit/sagemaker/experiments --ignore tests/unit/sagemaker/local \
    --ignore tests/unit/sagemaker/monitor/test_data_capture_config.py --ignore tests/unit/sagemaker/experiments --ignore tests/unit/sagemaker/remote_function \
    --ignore tests/unit/sagemaker/model/test_deploy.py --deselect tests/unit/test_estimator.py::test_insert_invalid_source_code_args \
    --deselect tests/unit/sagemaker/tensorflow/test_estimator.py::test_insert_invalid_source_code_args || exit $?
