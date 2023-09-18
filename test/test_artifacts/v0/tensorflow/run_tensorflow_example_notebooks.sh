#!/bin/bash

# Create an empty notebook file for papermill's output
touch nb_output.ipynb

# List of all referenced notebook files in Basics, Core, and In Depth sections of Tensorflow docs, excluding experimentals.
# https://www.tensorflow.org/guide
example_notebooks=('basics.ipynb'
    'tensor.ipynb'
    'variable.ipynb'
    'autodiff.ipynb'
    'intro_to_graphs.ipynb'
    'intro_to_modules.ipynb'
    'basic_training_loops.ipynb'
    'core/quickstart_core.ipynb'
    'core/logistic_regression_core.ipynb'
    'core/mlp_core.ipynb'
    'core/matrix_core.ipynb'
    'core/optimizers_core.ipynb'
    'tensor_slicing.ipynb'
    'advanced_autodiff.ipynb'
    'ragged_tensor.ipynb'
    'sparse_tensor.ipynb'
    'random_numbers.ipynb'
)

for nb in ${example_notebooks[@]}; do
     papermill $nb 'nb_output.ipynb'
done
