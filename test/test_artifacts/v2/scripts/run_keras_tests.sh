#!/bin/bash

keras_version=$(micromamba list | grep keras | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$keras_version
# Ref: https://keras.io/guides/, https://github.com/keras-team/keras-io/tree/master
for file in *.py; do
    if [ "$file" != "transfer_learning.py" ] && [ "$file" != "custom_train_step_in_torch.py" ]; then
        # skipping transfer_learning.py because it has 20 epochs and it takes a very long time to execute
        # https://github.com/keras-team/keras-io/blob/master/guides/transfer_learning.py#L562
	# skipping custom_train_step_in_torch.py because there is a bug which causes error
        python "$file" || exit $?
    fi
done
