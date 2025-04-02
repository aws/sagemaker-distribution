#!/bin/bash

pysdk_version=$(micromamba list | grep supervisor | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pysdk_version

pytest -v supervisor/tests/

