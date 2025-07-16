#!/bin/bash
set -eu

# Get project directory based on storage type
PROJECT_DIR=${SMUS_PROJECT_DIR:-"$HOME/src"}
MOUNT_DIR=$(readlink -f "$PROJECT_DIR")  # get the symlink source if it's symlink

# Datazone project metadata
RESOURCE_METADATA_FILE=/opt/ml/metadata/resource-metadata.json
SM_DOMAIN_ID=$(jq -r ".DomainId" < $RESOURCE_METADATA_FILE)
AWS_ACCOUNT_ID=$(jq -r '.ExecutionRoleArn | split(":")[4]' < $RESOURCE_METADATA_FILE)
ECR_ACCOUNT_ID=058264401727
DZ_DOMAIN_ID=$(jq -r '.AdditionalMetadata.DataZoneDomainId' < $RESOURCE_METADATA_FILE)
DZ_PROJECT_ID=$(jq -r '.AdditionalMetadata.DataZoneProjectId' < $RESOURCE_METADATA_FILE)
DZ_ENV_ID=$(jq -r '.AdditionalMetadata.DataZoneEnvironmentId' < $RESOURCE_METADATA_FILE)
DZ_DOMAIN_REGION=$(jq -r '.AdditionalMetadata.DataZoneDomainRegion' < $RESOURCE_METADATA_FILE)
DZ_ENDPOINT=$(jq -r '.AdditionalMetadata.DataZoneEndpoint' < $RESOURCE_METADATA_FILE)
DZ_PROJECT_S3PATH=$(jq -r '.AdditionalMetadata.ProjectS3Path' < $RESOURCE_METADATA_FILE)

# Workflows paths in JL
WORKFLOW_DAG_PATH="${PROJECT_DIR}/workflows/dags"
WORKFLOW_CONFIG_PATH="${PROJECT_DIR}/workflows/config"
WORKFLOW_DB_DATA_PATH="$HOME/.workflows_setup/db-data"
WORKFLOW_REQUIREMENTS_PATH="$HOME/.workflows_setup/requirements/"
WORKFLOW_PLUGINS_PATH="$HOME/.workflows_setup/plugins"
WORKFLOW_STARTUP_PATH="$HOME/.workflows_setup/startup/"
WORKFLOW_ARTIFACTS_SOURCE_DIR="/etc/sagemaker-ui/workflows"
WORKFLOW_PLUGINS_SOURCE_PATH="${WORKFLOW_ARTIFACTS_SOURCE_DIR}/plugins/*.whl"
WORKFLOW_REQUIREMENTS_SOURCE_PATH="${WORKFLOW_ARTIFACTS_SOURCE_DIR}/requirements/requirements.txt"
WORKFLOW_AIRFLOW_REQUIREMENTS_SOURCE_PATH="/etc/sagemaker-ui/workflows/requirements/requirements.txt"
WORKFLOW_OUTPUT_PATH="$HOME/jobs"
USER_REQUIREMENTS_FILE="${WORKFLOW_CONFIG_PATH}/requirements.txt"
USER_PLUGINS_FOLDER="${WORKFLOW_CONFIG_PATH}/plugins"
USER_STARTUP_FILE="${WORKFLOW_CONFIG_PATH}/startup.sh"


handle_workflows_startup_error() {
    local step=$1
    local detailed_status=""
    case $step in
        0)
            detailed_status="Workflows blueprint not enabled"
            ;;
        1)
            detailed_status="Not enough memory"
            ;;
        2)
            detailed_status="Error creating directories"
            ;;
        3)
            detailed_status="Error installing docker"
            ;;
        4)
            detailed_status="Error copying prerequisite files"
            ;;
        5)
            detailed_status="Error starting workflows image"
            # Kill any orphans that may have started
            python /etc/sagemaker-ui/workflows/workflow_client.py stop-local-runner
            ;;
        *)
            detailed_status="Unknown error"
            ;;
    esac
    python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'unhealthy' --detailed-status "$detailed_status"
    exit 1
}

# Create status log file if it doesn't exist
WORKFLOW_HEALTH_PATH="$HOME/.workflows_setup/health"
mkdir -p $WORKFLOW_HEALTH_PATH
if [ ! -f "${WORKFLOW_HEALTH_PATH}/status.json" ]; then
    echo "Creating status file"
    echo "[]" > "${WORKFLOW_HEALTH_PATH}/status.json"
fi

# Only start local runner if Workflows blueprint is enabled
if  [ "$(python /etc/sagemaker-ui/workflows/workflow_client.py check-blueprint --region "$DZ_DOMAIN_REGION" --domain-id "$DZ_DOMAIN_ID" --endpoint "$DZ_ENDPOINT")" = "False" ]; then
    echo "Workflows blueprint is not enabled. Workflows will not start."
    handle_workflows_startup_error 0
fi

# Do minimum system requirements check: 4GB RAM and more than 2 CPU cores
free_mem=$(free -m | awk '/^Mem:/ {print $7}')
cpu_cores=$(nproc)
if [[ $free_mem -lt 4096 ]] || [[ $cpu_cores -le 2 ]]; then
    echo "There is less than 4GB of available RAM or <=2 CPU cores. Workflows will not start. Free mem: $free_mem MB, CPU cores: $cpu_cores"
    handle_workflows_startup_error 1
fi

(
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'starting' --detailed-status 'Creating directories'

# Create necessary directories
mkdir -p $WORKFLOW_DAG_PATH
mkdir -p $WORKFLOW_CONFIG_PATH
mkdir -p $WORKFLOW_DB_DATA_PATH
mkdir -p $WORKFLOW_REQUIREMENTS_PATH
mkdir -p $WORKFLOW_PLUGINS_PATH
mkdir -p $WORKFLOW_STARTUP_PATH
mkdir -p $WORKFLOW_OUTPUT_PATH
) || handle_workflows_startup_error 2

(
# Set the status of the status file to 'starting'
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'starting' --detailed-status 'Installing prerequisites'

# Workflows execution environment install
sudo apt-get update
sudo install -m 0755 -d /etc/apt/keyrings
sudo rm -f /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
VERSION_ID=$(cat /etc/os-release | grep -oP 'VERSION_ID=".*"' | cut -d'"' -f2)
VERSION_STRING=$(sudo apt-cache madison docker-ce | awk '{ print $3 }' | grep -i $VERSION_ID | head -n 1)
sudo apt-get install docker-ce-cli=$VERSION_STRING docker-compose-plugin=2.29.2-1~ubuntu.22.04~jammy -y --allow-downgrades
) || handle_workflows_startup_error 3

(
# Set status to copying files
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'starting' --detailed-status 'Copying files'

# Create .airflowignore file
cat >>"$WORKFLOW_DAG_PATH/.airflowignore" <<'END'
.ipynb_checkpoints
END

#copy plugins from conda
cp $WORKFLOW_PLUGINS_SOURCE_PATH $WORKFLOW_PLUGINS_PATH
#copy requirements from conda
cp $WORKFLOW_REQUIREMENTS_SOURCE_PATH $WORKFLOW_REQUIREMENTS_PATH

# Copy system startup
cp /etc/sagemaker-ui/workflows/startup/startup.sh $WORKFLOW_STARTUP_PATH

# Append user's custom startup script, if exists
if [ -f $USER_STARTUP_FILE ]; then
    tail -n +2 $USER_STARTUP_FILE >> "${WORKFLOW_STARTUP_PATH}startup.sh"
else
    # Give the user a template startup script
    echo "#!/bin/bash" > "${USER_STARTUP_FILE}"
    echo "# Place any special instructions you'd like run during your workflows environment startup here" >> "${USER_STARTUP_FILE}"
    echo "# Note that you will need to restart your space for changes to take effect." >> "${USER_STARTUP_FILE}"
    echo "# For example:" >> "${USER_STARTUP_FILE}"
    echo "# pip install dbt-core" >> "${USER_STARTUP_FILE}"
fi

# Append user's custom requirements, if exists
if [ -f $USER_REQUIREMENTS_FILE ]; then
    cat $USER_REQUIREMENTS_FILE >> "${WORKFLOW_REQUIREMENTS_PATH}requirements.txt"
else
    # Give the user a template requirements.txt file
    echo "# Place any requirements you'd like included in your workflows environment here" > "${USER_REQUIREMENTS_FILE}"
    echo "# Note that you will need to restart your space for changes to take effect." >> "${USER_REQUIREMENTS_FILE}"
    echo "# For example:" >> "${USER_REQUIREMENTS_FILE}"
    echo "# numpy==1.26.4" >> "${USER_REQUIREMENTS_FILE}"
fi

# Copy over any user-specified plugins, if they exist
if [ -d $USER_PLUGINS_FOLDER ]; then
    cp -r $USER_PLUGINS_FOLDER/* $WORKFLOW_PLUGINS_PATH
fi

) || handle_workflows_startup_error 4

(
# Set status to installing workflows image
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'starting' --detailed-status 'Installing workflows image'

# Copy sample dag if it does not exist
cp -n "/etc/sagemaker-ui/workflows/sample_dag.py" "${WORKFLOW_DAG_PATH}/"

# Log into ECR repository
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

PROJECT_DIR=$(basename $PROJECT_DIR)  \
MOUNT_DIR=$MOUNT_DIR \
ECR_ACCOUNT_ID=$ECR_ACCOUNT_ID \
ACCOUNT_ID=$AWS_ACCOUNT_ID \
DZ_DOMAIN_ID=$DZ_DOMAIN_ID \
DZ_PROJECT_ID=$DZ_PROJECT_ID \
DZ_ENV_ID=$DZ_ENV_ID \
DZ_DOMAIN_REGION=$DZ_DOMAIN_REGION \
DZ_PROJECT_S3PATH=$DZ_PROJECT_S3PATH \
  docker compose -f /etc/sagemaker-ui/workflows/docker-compose.yaml up -d --quiet-pull
) || handle_workflows_startup_error 5

# Set status to waiting for image to start
python /etc/sagemaker-ui/workflows/workflow_client.py update-local-runner-status --status 'starting' --detailed-status 'Waiting for workflows image to start'

# Start healthchecker
sleep 30 # give the container some time to start
supervisorctl -s unix:///var/run/supervisord/supervisor.sock start workflows_healthcheck
