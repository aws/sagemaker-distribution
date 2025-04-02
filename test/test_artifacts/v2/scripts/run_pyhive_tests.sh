#!/bin/bash

pyhive_version=$(micromamba list | grep pyhive | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pyhive_version

./scripts/make_test_tables.sh

pip install -r dev_requirements.txt

pytest -v pyhive/tests/test_common.py