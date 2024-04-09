#!/bin/bash

SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}')
pytest -vv -r ap $SITE_PACKAGES/data_explorer || exit $?
