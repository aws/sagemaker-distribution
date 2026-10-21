#!/bin/bash

set -e

# Run examples for pytorch and sklearn.
# v5 images do not ship TensorFlow, so the keras (tensorflow.keras) and tensorflow examples are not run.
cd examples

# pytorch
cd pytorch/
python mnist_tensorboard_artifact.py
cd -

# sklearn
for folder in "sklearn_autolog/" "sklearn_elasticnet_diabetes/linux/" "sklearn_elasticnet_wine/" "sklearn_logistic_regression/"; do
  cd ${folder}
  for file in *.py; do
    python "$file" || exit $?
  done
  cd -
done
