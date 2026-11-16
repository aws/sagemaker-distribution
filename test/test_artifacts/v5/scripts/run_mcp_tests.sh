#!/bin/bash

# We need to checkout the version of mcp python-sdk that is installed in the mamba environment.
mcp_version=$(micromamba list | grep ' mcp ' | tr -s ' ' | cut -d ' ' -f 3)

# Checkout the corresponding mcp python-sdk version
git checkout tags/v$mcp_version

pytest tests/server tests/issues tests/shared || exit $?