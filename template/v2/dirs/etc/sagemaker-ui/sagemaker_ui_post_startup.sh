#!/bin/bash
set -eux

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

# Generate sagemaker pysdk intelligent default config
nohup python /etc/sagemaker/sm_pysdk_default_config.py &

# Start workflows local runner
bash /etc/sagemaker-ui/workflows/start-workflows-container.sh

# Install conda and pip dependencies if lib mgmt config existing
bash /etc/sagemaker-ui/libmgmt/install-lib.sh $HOME/src

# Install sm-spark-cli
bash /etc/sagemaker-ui/workflows/sm-spark-cli-install.sh