#!/bin/bash

# Expected output
expected_output=$'channels:\n  - conda-forge'

# Actual output
actual_micromamba=$(micromamba config list channels)
actual_conda=$(conda config --show channels)

# Compare the outputs
if [ "$actual_micromamba" = "$expected_output" ]; then
    echo "Micromamba Validation passed: Output matches expected format"
    exit 0
else
    echo "Micromamba Validation failed: Output does not match expected format"
    echo "Expected:"
    echo "$expected_output"
    echo "Actual:"
    echo "$actual_micromamba"
    exit 1
fi

# Compare the outputs
if [ "$actual_conda" = "$expected_output" ]; then
    echo "Conda Validation passed: Output matches expected format"
    exit 0
else
    echo "Conda Validation failed: Output does not match expected format"
    echo "Expected:"
    echo "$expected_output"
    echo "Actual:"
    echo "$actual_conda"
    exit 1
fi
