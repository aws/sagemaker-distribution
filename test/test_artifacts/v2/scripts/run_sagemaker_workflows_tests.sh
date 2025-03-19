#!/bin/bash

# Check successful completion of post-launch script
/etc/sagemaker-ui/sagemaker_ui_post_startup.sh

# Give the local runner 3 mins to start
sleep 180

# Check if airflow APIs are running and returning valid responses
curl -s http://default:8888/jupyterlab/default/proxy/absolute/8080/api/v1/dags | jq -e 'has("dags")'

# Check that healthchecker is running
HC_STATUS=$(supervisorctl -s unix:///var/run/supervisord/supervisor.sock status workflows_healthcheck | awk '{print $2}')
test [[ $HC_STATUS = "RUNNING" ]]

# Check if workflows toolkit contains workflows feature
sagemaker-ui-helper list executions | jq -e '[]'
