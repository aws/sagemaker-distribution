#!/bin/bash

kernel_type=$2
connection_file=$4

sparkmagicHomeDir=/home/sagemaker-user/.sparkmagic
mkdir -p $sparkmagicHomeDir
config_file_path=${sparkmagicHomeDir}/config.json
if [ ! -f "$config_file_path" ]; then
    cat << EOT > "$config_file_path"
{
    "livy_session_startup_timeout_seconds": 180,
    "logging_config": {
      "version": 1,
      "formatters": {
        "magicsFormatter": {
          "format": "%(asctime)s\t%(levelname)s\t%(message)s",
          "datefmt": ""
        }
      },
      "handlers": {
        "magicsHandler": {
          "class": "sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager.common.logger_utils.SessionManagerFileHandler",
          "formatter": "magicsFormatter",
          "file_name": "spark_magic"
        }
      },
      "loggers": {
        "magicsLogger": {
          "handlers": ["magicsHandler"],
          "level": "INFO",
          "propagate": 0
        }
      }
    }
}
EOT
else
    sed -i 's/\"sagemaker_base_session_manager/\"sagemaker_studio_dataengineering_sessions.sagemaker_base_session_manager/g' $config_file_path
fi
exec /opt/conda/bin/python -m ${kernel_type} -f ${connection_file}
