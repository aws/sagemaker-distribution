#!/bin/bash
set -e

POLLING_INTERVAL=1 # seconds
LOCAL_RUNNER_HEALTH_ENDPOINT="http://default:8888/jupyterlab/default/proxy/absolute/8080/api/v1/health"

while true; do
    response=$(curl -s -w "%{http_code}" $LOCAL_RUNNER_HEALTH_ENDPOINT)
    curl_exit_code=$?

    if [[ $curl_exit_code -ne 0 ]]; then
        python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'unhealthy' --detailed-status 'Local runner health endpoint is unreachable'
    else

        http_code=${response: -3}
        body=${response:0:${#response}-3}

        if [[ $http_code -ne 200 ]]; then
            python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'unhealthy' --detailed-status 'Local runner health endpoint is unreachable'
        elif [[ -z "$body" ]]; then
            python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'unhealthy' --detailed-status 'Local runner health endpoint did not return a response'
        else
            status=$(echo $body | jq -r '.metadatabase.status, .scheduler.status, .triggerer.status, .dag_processor.status')
            if [[ "$status" == *"unhealthy"* ]]; then
                python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'unhealthy' --detailed-status 'Local runner is unhealthy'
            else
                python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'healthy' --detailed-status 'Local runner is healthy'
                POLLING_INTERVAL=10 # raise to 10 seconds after startup
            fi
        fi
    fi

    sleep $POLLING_INTERVAL
done
