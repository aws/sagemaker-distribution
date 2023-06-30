#!/bin/bash

AUTOGLUON_VERSION=$(micromamba list | grep autogluon.tabular | tr -s ' ' | cut -d ' ' -f 3)
git checkout tags/v$AUTOGLUON_VERSION

# Don't run tests with optional dependencies not install from conda build
SELECT_TESTS='not automm_sts and not image_predictor and not tabpfn and not vowpalwabbit and not (tabular_nn and compile_onnx)'
pytest tabular/tests/unittests/models/ -k "$SELECT_TESTS" || exit $?
