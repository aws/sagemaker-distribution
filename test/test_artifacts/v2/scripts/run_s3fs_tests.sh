#!/bin/bash

# We need to checkout the version of s3fs that is installed in the mamba environment.
s3fs_version=$(micromamba list | grep s3fs | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding s3fs source code
git checkout tags/$s3fs_version

# Install requirements
# Remove portion incompatible with conda/mamba
sed -i "s/; python_version < '3.3'//" test_requirements.txt
# For <2024.10.0, there's no upperbound on moto.
# This causes test failures, so we add the upperbound.
# https://github.com/fsspec/s3fs/pull/917/files#diff-25d7875059b9486b7912948b78c0bb1c763d565fe0d12dc8287b5f0dc9982176L17
if [[ "$s3fs_version" == "2024.10.0" ]]; then
    sed -i "s/moto>=4/moto>=4,<5/" test_requirements.txt
fi
micromamba install --freeze-installed -y --file test_requirements.txt

pytest || exit $?