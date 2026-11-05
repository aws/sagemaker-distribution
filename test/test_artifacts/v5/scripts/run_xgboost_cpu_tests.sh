#!/bin/bash

# v5 installs the `xgboost` metapackage (build cpu_*/cuda*) instead of py-xgboost-cpu.
xgboost_version=$(micromamba list | awk '$1=="xgboost" {print $2}')

git checkout tags/v$xgboost_version

python -m pytest tests/python/test_config.py -v -k "not test_nthread"
python -m pytest tests/python/test_demos.py -v
python -m pytest tests/python/test_basic_models.py -v -k "not test_custom_objective"

#skipping nthread and test_custome_obejective due to need of nthread variable and logreboj
