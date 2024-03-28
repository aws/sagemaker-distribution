#!/bin/bash

check_key() {
    local json="$1"
    local full_key="$2"

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

    return 0  # Key exists
}

kernel_type=$2
connection_file=$4

glue_connection=`maxdome-toolkit connection read -n $MAXDOME_CONNECTION_NAME -ws`
export glue_role_arn=$(echo "$glue_connection" | jq .environmentRoleArn -r)
export AWS_REGION=$(echo "$glue_connection" | jq .location.awsRegion -r)

if check_key "$glue_connection" "sparkGlueProperties.glueConnection.Name"; then
    export glue_connections=$(echo "$glue_connection" | jq .sparkGlueProperties.glueConnection.Name -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.glue_version"; then
    export glue_version=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.glue_version -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.spark_conf"; then
    export glue_spark_conf=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.spark_conf -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.session_type"; then
    export glue_session_type=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.session_type -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.extra_py_files"; then
    export extra_py_files=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.session_type -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.additional_python_modules"; then
    export additional_python_modules=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.session_type -r)
fi

if check_key "$glue_connection" "sparkGlueProperties.sessionConfigs.extra_jars"; then
    export extra_jars=$(echo "$glue_connection" | jq .sparkGlueProperties.sessionConfigs.session_type -r)
fi

/opt/conda/bin/python -m "${kernel_type}" -f "${connection_file}"
