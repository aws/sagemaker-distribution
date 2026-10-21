#!/bin/bash
# v5 images have no TensorFlow or JAX; the Dockerfile sets KERAS_BACKEND=torch.
keras_version=$(micromamba list | awk '$1=="keras" {print $2}')

git checkout tags/v$keras_version
# Ref: https://keras.io/guides/, https://github.com/keras-team/keras-io/tree/master
for file in *.py; do
    case "$file" in
        *_in_tensorflow.py | *_with_tensorflow.py | *_in_jax.py | *_with_jax.py)
            # Backend-specific guides for backends that are not installed.
            continue ;;
        transfer_learning.py)
            # 20 epochs, takes a very long time to execute
            # https://github.com/keras-team/keras-io/blob/master/guides/transfer_learning.py#L562
            continue ;;
        distributed_training_with_torch.py)
            # Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method
            continue ;;
        custom_train_step_in_torch.py)
            # AttributeError: 'list' object has no attribute 'shape'
            continue ;;
        writing_a_custom_training_loop_in_torch.py)
            # Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
            continue ;;
    esac
    echo "Running $file"
    python "$file" || exit $?
done
