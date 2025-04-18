#!/bin/bash
set -eux

# Writes script status to file. This file is read by an IDE extension responsible for dispatching UI post-startup-status to the user.
write_status_to_file() {
    local status="$1"
    local message="$2"
    local file="/tmp/.post-startup-status.json"

    # Check if the file exists, if not, create it
    if [ ! -f "$file" ]; then
        touch "$file" || {
            echo "Failed to create $file" >&2
            return 0
        }
    fi

    # Ensure the file is writable
    if [ ! -w "$file" ]; then
        echo "Error: $file is not writable" >&2
        return 0
    fi

    # Create the JSON object and write to file
    jq -n --arg status "$status" --arg message "$message" '{"status":$status,"message":$message}' > "$file"

}

# checks if the script status is "in-progress". If so, no errors were detected and it can be marked successful.
write_status_to_file_on_script_complete() {
    local file="/tmp/.post-startup-status.json"
    local check_key="status"
    local check_value="in-progress"


    if jq -e --arg key "$check_key" --arg value "$check_value" '.[$key] == $value' "$file" > /dev/null; then
        write_status_to_file "success" "IDE configured successfully."
        echo "Post-startup script completed successfully. Success status written to $file"
    else
        echo "Skipping writing post-startup script "success" status. An error was detected during execution and written to $file".
    fi
}

write_status_to_file "in-progress" "IDE configuration in progress."

sourceMetaData=/opt/ml/metadata/resource-metadata.json

# Extract the required fields from meta data stored in opt/ml/metadata.
dataZoneDomainId=$(jq -r '.AdditionalMetadata.DataZoneDomainId' < $sourceMetaData)
dataZoneUserId=$(jq -r '.AdditionalMetadata.DataZoneUserId' < $sourceMetaData)
dataZoneProjectRepositoryName=$(jq -r '.AdditionalMetadata.DataZoneProjectRepositoryName' < $sourceMetaData)
dataZoneEndPoint=$(jq -r '.AdditionalMetadata.DataZoneEndpoint' < $sourceMetaData)
dataZoneProjectId=$(jq -r '.AdditionalMetadata.DataZoneProjectId' < $sourceMetaData)
dataZoneDomainRegion=$(jq -r '.AdditionalMetadata.DataZoneDomainRegion' < $sourceMetaData)

set +e

# Creating a directory where the repository will be cloned
mkdir -p $HOME/src

# Remove the ~/.aws/config file to start clean when space restart
rm -f /home/sagemaker-user/.aws/config
echo "Successfully removed the ~/.aws/config file"

aws configure set credential_source EcsContainer
echo "Successfully configured default profile"

# add SparkMonitor and Connection Magic entrypoint
NB_USER=sagemaker-user

config_path=/home/${NB_USER}/.ipython/profile_default/ipython_config.py

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

# Setting this to +x to not log credentials from the response of fetching credentials.
set +x

# Note: The $? check immediately follows the sagemaker-studio command to ensure we're checking its exit status.
# Adding commands between these lines could lead to incorrect error handling.
response=$( sagemaker-studio credentials get-domain-execution-role-credential-in-space --domain-id "$dataZoneDomainId" --profile default)
responseStatus=$?

set -x

if [ $responseStatus -ne 0 ]; then
        echo "Failed to fetch domain execution role credentials. Will skip adding new credentials profile: DomainExecutionRoleCreds."
        write_status_to_file "error" "Network issue detected. Your domain may be using a public subnet, which affects IDE functionality. Please contact your administrator."
else
        aws configure set credential_process "sagemaker-studio credentials get-domain-execution-role-credential-in-space --domain-id $dataZoneDomainId --profile default" --profile DomainExecutionRoleCreds
        echo "Successfully configured DomainExecutionRoleCreds profile"
fi

echo "Starting execution of Git Cloning script"
bash /etc/sagemaker-ui/git_clone.sh

# Run AWS CLI command to get the username from DataZone User Profile.
if [ ! -z "$dataZoneEndPoint" ]; then
    response=$( aws datazone get-user-profile --endpoint-url "$dataZoneEndPoint" --domain-identifier "$dataZoneDomainId" --user-identifier "$dataZoneUserId" --region "$dataZoneDomainRegion" )
else
    response=$( aws datazone get-user-profile --domain-identifier "$dataZoneDomainId" --user-identifier "$dataZoneUserId" --region "$dataZoneDomainRegion" )
fi

# Extract the Auth Mode from the response. Unified Studio currently supports IAM, SSO and SAML.
auth_mode=$(echo "$response" | jq -r '.type')

case "$auth_mode" in
    "IAM")
        # For IAM users - extract IAM ARN from response. Response does not contain username or email.
        arn=$(echo "$response" | jq -r '.details.iam.arn')
        # Split ARN by / and return the last field
        username=$(echo "$arn" | awk -F'/' '{print $NF}')
        email="$arn"
        ;;
    "SSO"|"SAML")
        # For SSO and SAML user, extract username and email if present in response.
        username=$(echo "$response" | jq -r '.details.sso.username')
        email=$(echo "$response" | jq -r '.details.sso.email')
        # Setting up the email as username if email is not present
        if [ -z "$email" ] || [ "$email" = "null" ]; then
            email="$username"
        fi
        ;;
    *)
        echo "Unknown authentication mode: $auth_mode"
        exit 1
        ;;
esac

# Setting up the Git identity for the user .
git config --global user.email "$email"
git config --global user.name "$username"

# MLFlow tracking server uses the LOGNAME environment variable to track identity. Set the LOGNAME to the username of the user associated with the space
export LOGNAME=$username
if grep -q "^LOGNAME=" ~/.bashrc; then
  echo "LOGNAME is defined in the env"
else
  echo LOGNAME=$username >> ~/.bashrc
  echo readonly LOGNAME >> ~/.bashrc
fi

set -e

# write unexpected error to file if any of the remaining scripts fail.
trap 'write_status_to_file "error" "An unexpected error occurred. Please stop and restart your space to retry."' ERR

# Generate sagemaker pysdk intelligent default config
nohup python /etc/sagemaker/sm_pysdk_default_config.py &
# Only run the following commands if SAGEMAKER_APP_TYPE_LOWERCASE is jupyterlab
if [ "${SAGEMAKER_APP_TYPE_LOWERCASE}" = "jupyterlab" ]; then
    # Start workflows local runner
    bash /etc/sagemaker-ui/workflows/start-workflows-container.sh

    # Install conda and pip dependencies if lib mgmt config existing
    bash /etc/sagemaker-ui/libmgmt/install-lib.sh $HOME/src

    # Install sm-spark-cli
    bash /etc/sagemaker-ui/workflows/sm-spark-cli-install.sh
fi

write_status_to_file_on_script_complete