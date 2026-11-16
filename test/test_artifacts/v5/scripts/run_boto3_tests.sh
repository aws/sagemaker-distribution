#!/bin/bash

# We need to checkout the version of boto3 that is installed in the mamba environment.

boto3_version=$(micromamba list | grep boto3 | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding boto3 version
git checkout tags/$boto3_version

# Run the unit and functional tests
pytest tests/unit tests/functional || exit $?
