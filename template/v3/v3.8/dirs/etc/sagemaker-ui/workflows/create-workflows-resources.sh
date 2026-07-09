#!/bin/bash
set -eu

# Get project directory based on storage type
PROJECT_DIR=${SMUS_PROJECT_DIR:-"$HOME/src"}
if [ -z "${SMUS_PROJECT_DIR:-}" ]; then
    MOUNT_DIR=$PROJECT_DIR
else
    MOUNT_DIR=$(readlink -f "$PROJECT_DIR")  # get the symlink source
fi

# Datazone project metadata
RESOURCE_METADATA_FILE=/opt/ml/metadata/resource-metadata.json

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
WORKFLOW_OUTPUT_PATH="$HOME/jobs"
USER_REQUIREMENTS_FILE="${WORKFLOW_CONFIG_PATH}/requirements.txt"
USER_PLUGINS_FOLDER="${WORKFLOW_CONFIG_PATH}/plugins"
USER_STARTUP_FILE="${WORKFLOW_CONFIG_PATH}/startup.sh"

# Only proceed if Workflows blueprint is enabled
if  [ "$(python /etc/sagemaker-ui/workflows/workflow_client.py check-blueprint --region "$DZ_DOMAIN_REGION" --domain-id "$DZ_DOMAIN_ID" --endpoint "$DZ_ENDPOINT" --project-id "$DZ_PROJECT_ID")" = "False" ]; then
    echo "Workflows blueprint is not enabled. Skipping workflows resource creation."
    exit 0
fi

# Create necessary directories
mkdir -p $WORKFLOW_DAG_PATH
mkdir -p $WORKFLOW_CONFIG_PATH
mkdir -p $WORKFLOW_DB_DATA_PATH
mkdir -p $WORKFLOW_REQUIREMENTS_PATH
mkdir -p $WORKFLOW_PLUGINS_PATH
mkdir -p $WORKFLOW_STARTUP_PATH
mkdir -p $WORKFLOW_OUTPUT_PATH

# Copy sample dag if it does not exist
cp -n "/etc/sagemaker-ui/workflows/sample_dag.py" "${WORKFLOW_DAG_PATH}/"

# Create .airflowignore file
cat >>"$WORKFLOW_DAG_PATH/.airflowignore" <<'END'
.ipynb_checkpoints
END

# Copy plugins from conda
cp $WORKFLOW_PLUGINS_SOURCE_PATH $WORKFLOW_PLUGINS_PATH

# Copy requirements from conda
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
