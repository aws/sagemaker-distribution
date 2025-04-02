#!/bin/bash

pysdk_version=$(micromamba list | grep uvicorn | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pysdk_version

pip install -r requirements.txt

pytest tests -v -k "not test_main.py"
