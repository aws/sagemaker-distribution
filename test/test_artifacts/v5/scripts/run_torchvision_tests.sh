#!/bin/bash

set -e 

torchvision_version=$(micromamba list | awk '$1=="torchvision" {print $2}')

git checkout tags/v$torchvision_version

test_files=(
    "test/test_utils.py"
    "test/test_architecture_ops.py"
    "test/test_backbone_utils.py"
)

for test_file in "${test_files[@]}"; do
        pytest "$test_file" -v 
done
