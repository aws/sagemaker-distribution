#!/bin/bash
set -e

jupyterlab_git_version=$(micromamba list | awk '$1=="jupyterlab-git" {print $2}')

git checkout tags/v$jupyterlab_git_version

# Test the installed package. Building from source needs the full JS toolchain, so only install the test deps.
micromamba install --freeze-installed -y -c conda-forge pytest pytest-asyncio pytest-jupyter

pytest -v packages/core/tests/
