#!/bin/bash

xgboost_gpu_version=$(micromamba list | grep py-xgboost | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$xgboost_gpu_version

python -m pytest tests/python-gpu/test_gpu_basic_models.py -v
python -m pytest tests/python-gpu/test_gpu_data_iterator.py -v
python -m pytest tests/python-gpu/test_gpu_prediction.py -v