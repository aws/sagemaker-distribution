#!/bin/bash

PROJECT_DIR=${SMUS_PROJECT_DIR:-"$HOME/src"}
MOUNT_DIR=$(readlink -f "$PROJECT_DIR")  # get the symlink source if it's symlink

DOCKER_EXECUTABLE=$(which docker)

# Stop healthchecker
supervisorctl -s unix:///var/run/supervisord/supervisor.sock stop workflows_healthcheck

# Stop the containers
export MOUNT_DIR=$MOUNT_DIR
$DOCKER_EXECUTABLE compose -f /etc/sagemaker-ui/workflows/docker-compose.yaml down

# Update status to stopped
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'stopped' --detailed-status 'Shutdown completed'
