#!/bin/bash

jupyter_server_proxy_version=$(micromamba list | grep jupyter-server-proxy | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$jupyter_server_proxy_version

pip install ".[test]" 

test_files=(
    "tests/test_config.py"
    "tests/test_proxies.py"
    "tests/test_utils.py"
)

# Run each test file
for test_file in "${test_files[@]}"; do
    pytest -v "$test_file"
done
