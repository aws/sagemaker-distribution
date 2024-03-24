#!/bin/bash

pip install pytest-jupyter
pytest -vv -r ap /opt/conda/lib/python3.10/site-packages/maxdome_jupyter_server_extension || exit $?
