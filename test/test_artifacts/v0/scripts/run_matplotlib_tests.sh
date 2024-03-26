#!/bin/bash
# Run all the tutorials
for file in *.py; do
     python "$file" || exit $?
done
