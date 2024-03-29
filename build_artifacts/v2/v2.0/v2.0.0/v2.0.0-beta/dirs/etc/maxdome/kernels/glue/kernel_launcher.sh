#!/bin/bash

export_if_key_exists() {
    local json="$1"
    local full_key="$2"
    local env_var_name="$3"

    # Split the full key into an array
    IFS='.' read -r -a key_parts <<< "$full_key"

    local key
    local current_json="$json"
    for key in "${key_parts[@]}"; do
        # Check if current_json has the key
        if ! jq -e --arg key "$key" 'has($key)' <<< "$current_json" >/dev/null 2>&1; then
            return 1  # Key does not exist
        fi
        # Update current_json to the value of the current key
        current_json=$(jq --arg key "$key" '.[$key]' <<< "$current_json")
    done

    # Key exists
    export "$env_var_name"="$current_json"
    return 0  
}

kernel_type=$2
connection_file=$4

glue_connection=`maxdome-toolkit connection read -n $MAXDOME_CONNECTION_NAME -ws`
export glue_role_arn=$(echo "$glue_connection" | jq .environmentRoleArn -r)
export AWS_REGION=$(echo "$glue_connection" | jq .location.awsRegion -r)

export_if_key_exists "$glue_connection" "sparkGlueProperties.glueConnection.Name" "glue_connections" 

/opt/conda/bin/python -m "${kernel_type}" -f "${connection_file}"
