#!/bin/bash

pysdk_version=$(micromamba list | grep jupyter-git | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pysdk_version

pip install ".[test]"

pytest -v jupyterlab_git/tests/
