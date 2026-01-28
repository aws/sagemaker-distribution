#!/bin/bash

# We need to checkout the version of sagemaker-gen-ai-jupyterlab-extension python-sdk that is installed in the mamba environment.
sagemaker_gen_ai_jupyterlab_extension_version=$(micromamba list | grep ' sagemaker-gen-ai-jupyterlab-extension ' | tr -s ' ' | cut -d ' ' -f 3)

# Checkout the corresponding mcp python-sdk version
git checkout tags/v$sagemaker_gen_ai_jupyterlab_extension_version

pytest tests/server tests/issues tests/shared || exit $?