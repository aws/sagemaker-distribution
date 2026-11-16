#!/bin/bash

# We need to checkout the version of seaborn that is installed in the mamba environment.
seaborn_version=$(micromamba list | grep seaborn-base | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding seaborn source code
git checkout tags/v$seaborn_version

# There's a test issue that was fixed for 0.13.2 release but isn't in the tag
# https://github.com/mwaskom/seaborn/pull/3802
# Cherry pick works but fails to commit due to no git creds, for our test we can ignore the error.
if [[ "$seaborn_version" == "0.13.2" ]]; then
    git cherry-pick 385e54676ca16d0132434bc9df6bc41ea8b2a0d4 || true
fi

# Install test dependencies
# seaborn 0.13.2's test suite applies marks to fixtures, which pytest 9 rejects at collection time.
micromamba install -y -c conda-forge "pytest<9" pytest-cov pytest-xdist pandas-stubs

# seaborn 0.13.2's log-scale and theme tests assume pre-3.11 matplotlib behaviour, and test_weights uses an API
# removed from numpy 2.x; deselect them.
pytest -k "not test_log_scale and not test_theme_validation and not (TestKDEPlotBivariate and test_weights)" || exit $?