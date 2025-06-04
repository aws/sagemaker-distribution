#!/bin/bash
set -eux

# Check if the .libs.json file exists
if [ -e $1/.libs.json ]; then
  lib_config_json=`cat $1/.libs.json`

  apply_change_to_space=`echo $lib_config_json | jq -r '.ApplyChangeToSpace'`
  # Extract conda channels from the config, add `-c ` before each channel and join the strings
  conda_channels=`echo $lib_config_json | jq -r '.Python.CondaPackages.Channels | .[]' | sed 's/^/-c /g'`
  # Extract conda package spec from the config and join the strings
  conda_package=`echo $lib_config_json | jq -r '.Python.CondaPackages.PackageSpecs | .[]'`

  if [ ${apply_change_to_space} == "true" -a -n "$conda_package" ]; then
    # if conda package spec exists, install the packages
    micromamba install --freeze-installed -y $conda_channels $conda_package
  fi
fi