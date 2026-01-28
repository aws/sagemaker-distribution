#!/bin/bash

fastapi_version=$(micromamba list | grep fastapi | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$fastapi_version

pip install -r requirements-tests.txt

pytest tests/ -v -k "not test_tutorial"
