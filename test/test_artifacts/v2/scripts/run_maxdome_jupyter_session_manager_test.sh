!/bin/bash

pip install pytest-jupyter
SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}')
pytest -vv -r ap $SITE_PACKAGES/maxdome_jupyter_session_manager || exit $?
