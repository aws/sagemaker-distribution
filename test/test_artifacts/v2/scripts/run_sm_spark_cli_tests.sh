#!/bin/bash

# Check if sm-spark-cli is installed
if command -v sm-spark-cli >/dev/null 2>&1; then
    echo "sm-spark-cli is installed."
    exit 0
else
    echo "Error: sm-spark-cli is not installed." >&2
    exit 1
fi