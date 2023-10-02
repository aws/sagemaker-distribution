#!/bin/bash

# Ref: https://keras.io/guides/, https://github.com/keras-team/keras-io/tree/master

for file in *.py; do
    if [ "$file" != "transfer_learning.py" ]; then
        # skipping transfer_learning.py because it has 20 epochs and it takes a very long time to execute
        # https://github.com/keras-team/keras-io/blob/master/guides/transfer_learning.py#L562
        python "$file" || exit $?
    fi
done
