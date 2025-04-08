#!/bin/bash

pip install pytest
SITE_PACKAGES=$(pip show sagemaker-studio | grep Location | awk '{print $2}')
pytest -vv -r p $SITE_PACKAGES/sagemaker_studio || exit $?