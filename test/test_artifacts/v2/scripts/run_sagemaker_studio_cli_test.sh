#!/bin/bash

pip install pytest
SITE_PACKAGES=$(pip show sagemaker-studio-cli | grep Location | awk '{print $2}')
pytest -vv -r p $SITE_PACKAGES/sagemaker_studio_cli || exit $?