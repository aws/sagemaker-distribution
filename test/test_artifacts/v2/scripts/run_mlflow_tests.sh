#!/bin/bash

set -e

# Run examples for keras, pytorch, sklearn, tensorflow
cd examples

# keras
cd keras/
python train.py
cd -

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

# tensorflow
cd tensorflow/
python train.py
cd -
