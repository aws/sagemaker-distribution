#!/bin/bash

jupyter_git_version=$(micromamba list | grep jupyter-git | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$jupyter_git_version

pip install ".[test]"

pytest -v jupyterlab_git/tests/
