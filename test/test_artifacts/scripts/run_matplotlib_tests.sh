#!/bin/bash
# Run all the tutorials
for file in *.py; do
     python "$file"
     # exit based on the return code
     rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
done


