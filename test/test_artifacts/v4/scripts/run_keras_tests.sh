#!/bin/bash
export XLA_FLAGS="--xla_gpu_cuda_data_dir=/opt/conda"
keras_version=$(micromamba list | grep keras | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$keras_version
# Ref: https://keras.io/guides/, https://github.com/keras-team/keras-io/tree/master
for file in *.py; do
    if [ "$file" != "transfer_learning.py" ] &&
    # skipping transfer_learning.py because it has 20 epochs and it takes a very long time to execute
    # https://github.com/keras-team/keras-io/blob/master/guides/transfer_learning.py#L562
    [ "$file" != "distributed_training_with_torch.py" ] &&
    # skipping distributed_training_with_torch.py because there is a bug which causes error:
    # Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method
    [ "$file" != "custom_train_step_in_torch.py" ] &&
    # skipping custom_train_step_in_torch.py because there is a bug which causes error:
    # AttributeError: 'list' object has no attribute 'shape'
    [ "$file" != "writing_a_custom_training_loop_in_torch.py" ]; then
    # skipping writing_a_custom_training_loop_in_torch.py because there is a bug which causes error:
    # AttributeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
        python "$file" || exit $?
    fi
done
