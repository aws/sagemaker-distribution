#!/bin/bash

# Create a default aws profile in SM training container
aws configure set credential_source EcsContainer

# Create a default ipython profile and load extensions in SM processing container
NB_USER=sagemaker-user
config_path=/home/${NB_USER}/.ipython/profile_default/ipython_config.py
# SparkMonitor Widget and Connection Magic - create entrypoint
if [ ! -f "$config_path" ] || ! grep -q "sagemaker_studio_dataengineering_sessions" "$config_path"; then
  ipython profile create && echo "c.InteractiveShellApp.extensions.extend(['sagemaker_sparkmonitor.kernelextension','sagemaker_studio_dataengineering_sessions.sagemaker_connection_magic'])" >>  $config_path
  cat << EOT >> "$config_path"
c.Application.logging_config = {
    "loggers": {
        "": {
            "level": "INFO",
            # console handler is required to keep the default behavior of jupyter logging.
            # https://jupyter-server.readthedocs.io/en/latest/operators/configuring-logging.html
            "handlers": ["console"],
        },
    },
}
EOT
fi