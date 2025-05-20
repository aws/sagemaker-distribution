#!/bin/bash

set -e 

torchvision_version=$(micromamba list | grep torchvision | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$torchvision_version

test_files=(
    "test/test_utils.py"
    "test/test_architecture_ops.py"
    "test/test_backbone_utils.py"
)

for test_file in "${test_files[@]}"; do
        pytest "$test_file" -v 
done
