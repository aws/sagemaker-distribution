#!/bin/bash
set -e

jupyter_collaboration_version=$(micromamba list | awk '$1=="jupyter-collaboration" {print $2}')

git checkout tags/v$jupyter_collaboration_version

# Test the installed packages. `pip install ".[test]"` rebuilds the JS extensions from source, which needs a
# jupyterlab inside pip's isolated build env and fails. Install only the test dependencies of jupyter-server-ydoc.
micromamba install --freeze-installed -y -c conda-forge pytest pytest-asyncio pytest-jupyter pytest-timeout dirty-equals httpx-ws

pytest tests/ -v
