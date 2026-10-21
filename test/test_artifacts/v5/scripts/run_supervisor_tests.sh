#!/bin/bash

supervisor_version=$(micromamba list | grep supervisor | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$supervisor_version

pytest -v supervisor/tests/

