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

# Remove the ~/.aws/config file to start clean when space restart
rm -f /home/sagemaker-user/.aws/config
echo "Successfully removed the ~/.aws/config file"

aws configure set credential_source EcsContainer
echo "Successfully configured default profile"

# Add region configuration using REGION_NAME environment variable
aws configure set region "${REGION_NAME}"
echo "Successfully configured region to ${REGION_NAME}"

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

# Add debug call to get domain info
if [ ! -z "$dataZoneEndPoint" ]; then
    domain_response=$(aws datazone get-domain --debug --endpoint-url "$dataZoneEndPoint" --identifier "$dataZoneDomainId" --region "$dataZoneDomainRegion" 2>&1)

else
    domain_response=$(aws datazone get-domain --debug --identifier "$dataZoneDomainId" --region "$dataZoneDomainRegion" 2>&1)
fi

# Check if domain is in express mode
response_body=$(echo "$domain_response" | grep -A1 "Response body:" | tail -n1 | sed 's/^b'\''//;s/'\''$//')
# Remove leading/trailing whitespace and the 'b' prefix
cleaned_response=$(echo "$response_body" | sed 's/\\n//g')
is_express_mode=$(echo "$cleaned_response" | jq -r '.preferences.DOMAIN_MODE == "EXPRESS"')

if [ "$is_express_mode" = "true" ]; then
    echo "Domain is in express mode. Using default credentials"
    # Use default credentials - no additional configuration needed
    aws configure set credential_source EcsContainer --profile DomainExecutionRoleCreds
    echo "Successfully configured DomainExecutionRoleCreds profile with default credentials"
else
    echo "Domain is not in express mode"
    # Setting this to +x to not log credentials from the response of fetching credentials.
    set +x
    # Note: The $? check immediately follows the sagemaker-studio command to ensure we're checking its exit status.
    # Adding commands between these lines could lead to incorrect error handling.
    response=$(timeout 30 sagemaker-studio credentials get-domain-execution-role-credential-in-space --domain-id "$dataZoneDomainId" --profile default)
    responseStatus=$?

    set -x

    if [ $responseStatus -ne 0 ]; then
        echo "Failed to fetch domain execution role credentials. Will skip adding new credentials profile: DomainExecutionRoleCreds."
        write_status_to_file "error" "Network issue detected. Your domain may be using a public subnet, which affects IDE functionality. Please contact your admin."
    else
        aws configure set credential_process "sagemaker-studio credentials get-domain-execution-role-credential-in-space --domain-id $dataZoneDomainId --profile default" --profile DomainExecutionRoleCreds
        echo "Successfully configured DomainExecutionRoleCreds profile"
    fi
fi

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

# Checks if the project is using Git or S3 storage
is_s3_storage() {
  getProjectDefaultEnvResponse=$(sagemaker-studio project get-project-default-environment --domain-id "$dataZoneDomainId" --project-id "$dataZoneProjectId" --profile DomainExecutionRoleCreds)
  gitConnectionArn=$(echo "$getProjectDefaultEnvResponse" | jq -r '.provisionedResources[] | select(.name=="gitConnectionArn") | .value')
  codeRepositoryName=$(echo "$getProjectDefaultEnvResponse" | jq -r '.provisionedResources[] | select(.name=="codeRepositoryName") | .value')

  if [ -z "$gitConnectionArn" ] && [ -z "$codeRepositoryName" ]; then
      return 0
  else
      return 1
  fi
}

echo "Checking Project Storage Type"

# Execute once to store the result
is_s3_storage
is_s3_storage_flag=$?  # 0 if S3 storage, 1 if Git

if [ "$is_s3_storage_flag" -eq 0 ]; then
    export IS_GIT_PROJECT=false
    export SMUS_PROJECT_DIR="$HOME/shared"
    echo "Project is using S3 storage, project directory set to: $SMUS_PROJECT_DIR"
else
    export IS_GIT_PROJECT=true
    export SMUS_PROJECT_DIR="$HOME/src"
    echo "Project is using Git storage, project directory set to: $SMUS_PROJECT_DIR"
fi

if grep -q "^SMUS_PROJECT_DIR=" ~/.bashrc; then
  echo "SMUS_PROJECT_DIR is defined in the env"
else
  echo SMUS_PROJECT_DIR="$SMUS_PROJECT_DIR" >> ~/.bashrc
  echo readonly SMUS_PROJECT_DIR >> ~/.bashrc
fi

# Write SMUS_PROJECT_DIR to a JSON file to be accessed by JupyterLab Extensions
mkdir -p "$HOME/.config"  # Create config directory if it doesn't exist
jq -n \
  --arg smusProjectDirectory "$SMUS_PROJECT_DIR" \
  --arg isGitProject "$IS_GIT_PROJECT" \
  '{ 
    smusProjectDirectory: $smusProjectDirectory,
    isGitProject: ($isGitProject == "true")
  }' > "$HOME/.config/smus-storage-metadata.json"

if [ $is_s3_storage_flag -ne 0 ]; then
  # Creating a directory where the repository will be cloned
  mkdir -p "$HOME/src"

  echo "Starting execution of Git Cloning script"
  bash /etc/sagemaker-ui/git_clone.sh

  # Setting up the Git identity for the user .
  git config --global user.email "$email"
  git config --global user.name "$username"
else
  echo "Project is using Non-Git storage, skipping git repository setup and ~/src dir creation and creating README"
  bash /etc/sagemaker-ui/project-storage/create-storage-readme.sh
fi

# MLFlow tracking server uses the LOGNAME environment variable to track identity. Set the LOGNAME to the username of the user associated with the space
export LOGNAME=$username
if grep -q "^LOGNAME=" ~/.bashrc; then
  echo "LOGNAME is defined in the env"
else
  echo LOGNAME=$username >> ~/.bashrc
  echo readonly LOGNAME >> ~/.bashrc
fi

# Setup Q CLI auth mode
q_settings_file="$HOME/.aws/amazon_q/settings.json"
if [ -f "$q_settings_file" ]; then
    q_auth_mode=$(jq -r '.auth_mode' < $q_settings_file)
    if [ "$q_auth_mode" == "IAM" ]; then
        export AMAZON_Q_SIGV4=true
    else 
        export AMAZON_Q_SIGV4=false
    fi
else
    export AMAZON_Q_SIGV4=true
fi

if $AMAZON_Q_SIGV4; then
    if grep -q "^export AMAZON_Q_SIGV4=" ~/.bashrc; then
        echo "AMAZON_Q_SIGV4 is defined in the env"
    else
        echo export AMAZON_Q_SIGV4=$AMAZON_Q_SIGV4 >> ~/.bashrc
    fi
else 
    # Remove from .bashrc if it exists
    sed -i '/^export AMAZON_Q_SIGV4=/d' ~/.bashrc
fi

# Setup SageMaker MCP configuration
echo "Setting up SageMaker MCP configuration..."
mkdir -p $HOME/.aws/amazonq/
target_file="$HOME/.aws/amazonq/mcp.json"
source_file="/etc/sagemaker-ui/sagemaker-mcp/mcp.json"

if [ -f "$source_file" ]; then
    # Extract all servers from source configuration
    if [ -f "$target_file" ]; then
        # Target file exists - merge configurations
        echo "Existing MCP configuration found, merging configurations..."
        
        # Check if it's valid JSON first
        if jq empty "$target_file" 2>/dev/null; then
            # Initialize mcpServers object if it doesn't exist
            if ! jq -e '.mcpServers' "$target_file" >/dev/null 2>&1; then
                echo "Creating mcpServers object in existing configuration"
                jq '. + {"mcpServers":{}}' "$target_file" > "$target_file.tmp"
                mv "$target_file.tmp" "$target_file"
            fi
            
            servers=$(jq '.mcpServers | keys[]' "$source_file" | tr -d '"')
            
            # Add each server from source to target if it doesn't exist
            for server in $servers; do
                if ! jq -e ".mcpServers.\"$server\"" "$target_file" >/dev/null 2>&1; then
                    server_config=$(jq ".mcpServers.\"$server\"" "$source_file")
                    jq --arg name "$server" --argjson config "$server_config" \
                        '.mcpServers[$name] = $config' "$target_file" > "$target_file.tmp"
                    mv "$target_file.tmp" "$target_file"
                    echo "Added server '$server' to existing configuration"
                else
                    echo "Server '$server' already exists in configuration"
                fi
            done
        else
            echo "Warning: Existing MCP configuration is not valid JSON, replacing with default configuration"
            cp "$source_file" "$target_file"
        fi
    else
        # File doesn't exist, copy our configuration
        cp "$source_file" "$target_file"
        echo "Created new MCP configuration with default servers"
    fi
    
    echo "Successfully configured MCP for SageMaker"
else
    echo "Warning: MCP configuration file not found at $source_file"
fi

# Migrating MCP configuration to new config file
echo "Migrating MCP configuration to Amazon Q agents..."
agents_target_file="$HOME/.aws/amazonq/agents/default.json"
agents_source_file="/etc/sagemaker-ui/sagemaker-mcp/default.json"

if [ -f "$agents_source_file" ]; then
    mkdir -p "$HOME/.aws/amazonq/agents/"
    
    if [ -f "$agents_target_file" ]; then
        echo "Existing Amazon Q agents configuration found, merging mcpServers..."
        
        # Check if target file is valid JSON
        if jq empty "$agents_target_file" 2>/dev/null; then
            # Initialize mcpServers object if it doesn't exist in target
            if ! jq -e '.mcpServers' "$agents_target_file" >/dev/null 2>&1; then
                echo "Creating mcpServers object in existing agents configuration"
                jq '. + {"mcpServers":{}}' "$agents_target_file" > "$agents_target_file.tmp"
                mv "$agents_target_file.tmp" "$agents_target_file"
            fi
            
            # Add servers from source that don't exist in target and update tools
            if jq -e '.mcpServers' "$agents_source_file" >/dev/null 2>&1; then
                source_server_names=$(jq -r '.mcpServers | keys[]' "$agents_source_file")
                
                for server_name in $source_server_names; do
                    if ! jq -e ".mcpServers.\"$server_name\"" "$agents_target_file" >/dev/null 2>&1; then
                        # Server doesn't exist in target - add it
                        server_config=$(jq ".mcpServers.\"$server_name\"" "$agents_source_file")
                        jq --arg name "$server_name" --argjson config "$server_config" \
                            '.mcpServers[$name] = $config' "$agents_target_file" > "$agents_target_file.tmp"
                        mv "$agents_target_file.tmp" "$agents_target_file"
                        echo "Added server '$server_name' to agents configuration"
                        
                        # Check if source has tools that reference this server and add them
                        server_tool_ref="@$server_name"
                        if jq -e --arg tool "$server_tool_ref" '.tools | index($tool)' "$agents_source_file" >/dev/null 2>&1; then
                            # Initialize tools array if it doesn't exist
                            if ! jq -e '.tools' "$agents_target_file" >/dev/null 2>&1; then
                                jq '. + {"tools":[]}' "$agents_target_file" > "$agents_target_file.tmp"
                                mv "$agents_target_file.tmp" "$agents_target_file"
                            fi
                            
                            # Add tool reference if it doesn't exist
                            if ! jq -e --arg tool "$server_tool_ref" '.tools | index($tool)' "$agents_target_file" >/dev/null 2>&1; then
                                jq --arg tool "$server_tool_ref" '.tools += [$tool]' "$agents_target_file" > "$agents_target_file.tmp"
                                mv "$agents_target_file.tmp" "$agents_target_file"
                                echo "Added tool reference '$server_tool_ref' to agents configuration"
                            fi
                        fi
                    else
                        echo "Server '$server_name' already exists in configuration, skipping"
                    fi
                done
                
                echo "Successfully added missing mcpServers and tools from default.json to agents configuration"
            else
                echo "No mcpServers found in source configuration"
            fi
        else
            echo "Warning: Existing agents configuration is not valid JSON, replacing with default configuration"
            cp "$agents_source_file" "$agents_target_file"
        fi
    else
        cp "$agents_source_file" "$agents_target_file"
        echo "Created new Amazon Q agents configuration file"
    fi
    
    echo "Successfully migrated MCP configuration to Amazon Q agents"
else
    echo "Warning: Source configuration file not found at $agents_source_file"
fi

# Generate sagemaker pysdk intelligent default config
nohup python /etc/sagemaker/sm_pysdk_default_config.py &
# Only run the following commands if SAGEMAKER_APP_TYPE_LOWERCASE is jupyterlab and domain is not in express mode
if [ "${SAGEMAKER_APP_TYPE_LOWERCASE}" = "jupyterlab" ] && [ "$is_express_mode" != "true" ]; then
    # do not fail immediately for non-zero exit code returned
    # by start-workflows-container. An expected non-zero exit
    # code will be returned if there is not a minimum of 2
    # CPU cores available.
    # Start workflows local runner
    bash /etc/sagemaker-ui/workflows/start-workflows-container.sh

    # ensure functions inherit traps and fail immediately
    set -eE

    # write unexpected error to file if any of the remaining scripts fail.
    trap 'write_status_to_file "error" "An unexpected error occurred. Please stop and restart your space to retry."' ERR
    
    # Install conda and pip dependencies if lib mgmt config existing
    bash /etc/sagemaker-ui/libmgmt/install-lib.sh

    # Install sm-spark-cli
    bash /etc/sagemaker-ui/workflows/sm-spark-cli-install.sh
fi

# Execute network validation script, to check if any required AWS Services are unreachable
echo "Starting network validation script..."

network_validation_file="/tmp/.network_validation.json"

# Run the validation script; only if it succeeds, check unreachable services
if bash /etc/sagemaker-ui/network_validation.sh "$is_s3_storage_flag" "$network_validation_file"; then
    # Read unreachable services from JSON file
    failed_services=$(jq -r '.UnreachableServices // empty' "$network_validation_file" || echo "")
    if [[ -n "$failed_services" ]]; then
        # Count number of services by splitting on comma
        IFS=',' read -ra failed_array <<< "$failed_services"
        count=${#failed_array[@]}
        verb="are"
        [[ "$count" -eq 1 ]] && verb="is"

        error_message="$failed_services $verb unreachable. Please contact your admin."
        # Example error message: Redshift Clusters, Athena, STS, Glue are unreachable. Please contact your admin.
        write_status_to_file "error" "$error_message"
        echo "$error_message"
    fi
else
    echo "Warning: network_validation.sh failed, skipping unreachable services check."
fi

write_status_to_file_on_script_complete
