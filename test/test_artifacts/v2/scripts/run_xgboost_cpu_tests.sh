#!/bin/bash

pysdk_version=$(micromamba list | grep py-xgboost | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$pysdk_version

python -m pytest tests/python/test_config.py -v -k "not test_nthread"
python -m pytest tests/python/test_demos.py -v
python -m pytest tests/python/test_basic_models.py -v -k "not test_custom_objective"

#skipping nthread and test_custome_obejective due to need of nthread variable and logreboj