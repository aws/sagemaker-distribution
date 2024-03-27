#!/bin/bash

# We need to checkout the version of git-remote-codecommit that is installed in the mamba environment.

version=$(micromamba list | grep git-remote-codecommit | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding version
git checkout tags/$version

# Run the tests
pytest  test/git_url_test.py test/main_test.py || exit $?
