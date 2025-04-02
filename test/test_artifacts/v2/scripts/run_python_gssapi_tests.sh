#!/bin/bash

import_path=$(python -c "import gssapi; print(gssapi.__file__)")
gssapi_path=$(dirname "$import_path")
pip install k

echo "GSSAPI path: $gssapi_path"

# Run all tests
pytest -v "$gssapi_path"

