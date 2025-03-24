#!/bin/bash

pip install pytest pytest-jupyter
SITE_PACKAGES=$(pip show amzn-sagemaker-studio-dataengineering-extensions | grep Location | awk '{print $2}')
pytest -vv -r p $SITE_PACKAGES/sagemaker_studio_dataengineering_extensions || exit $?
