#!/bin/bash

pysdk_version=$(micromamba list | grep pyhive | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pysdk_version

./scripts/make_test_tables.sh

pip install -r dev_requirements.txt

pytest -v pyhive/tests/test_common.py