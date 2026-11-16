#!/bin/bash

notebook_version=$(micromamba list | grep notebook | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$notebook_version

pip install ".[test]"

pytest tests/ -v