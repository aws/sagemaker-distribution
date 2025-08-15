#!/bin/bash

DOCKER_EXECUTABLE=$(which docker)

# Stop healthchecker
supervisorctl -s unix:///var/run/supervisord/supervisor.sock stop workflows_healthcheck

# Stop the containers
$DOCKER_EXECUTABLE compose -f /etc/sagemaker-ui/workflows/docker-compose.yaml down

# Update status to stopped
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'stopped' --detailed-status 'Shutdown completed'
