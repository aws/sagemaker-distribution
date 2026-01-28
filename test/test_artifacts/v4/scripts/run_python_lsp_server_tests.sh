#!/bin/bash

# "Confirm that installation succeeded" by running this - https://github.com/python-lsp/python-lsp-server#installation
pylsp --help

python_lsp_server_version=$(micromamba list | grep python-lsp-server | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$python_lsp_server_version

pip install ".[test]"

pytest -v test/

