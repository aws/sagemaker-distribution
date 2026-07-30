#!/bin/bash
set -eux

sourceMetaData=/opt/ml/metadata/resource-metadata.json

# Extract the required fields from meta data stored in opt/ml/metadata.
dataZoneDomainId=$(jq -r '.AdditionalMetadata.DataZoneDomainId' < $sourceMetaData)
dataZoneUserId=$(jq -r '.AdditionalMetadata.DataZoneUserId' < $sourceMetaData)
dataZoneEndPoint=$(jq -r '.AdditionalMetadata.DataZoneEndpoint' < $sourceMetaData)
dataZoneProjectId=$(jq -r '.AdditionalMetadata.DataZoneProjectId' < $sourceMetaData)

DEFAULT_DESTINATION_PATH=$HOME/src
DESTINATION_PATH=${1:-$DEFAULT_DESTINATION_PATH}

echo "Cloning to ${DESTINATION_PATH}"

# Function to clone the CodeCommit repository
clone_code_commit_repo() {
    if [ -d "${DESTINATION_PATH}/.git" ]; then
        echo "Repository already exists at ${DESTINATION_PATH}"
    else
        rm -rf "${DESTINATION_PATH}"
        local repoName=$1
        git clone  codecommit::$AWS_REGION://$repoName $DESTINATION_PATH
        # if the above command exit with nonzero exit code ,delete the partially cloned Repo.
        if [ $? -ne 0 ]; then
            echo "Git clone of the Project repository has failed. Please refer to the documentation to understand how to fix this."
            if [ -d $DESTINATION_PATH ]; then
                rm -rf $DESTINATION_PATH
            fi
        fi
    fi
}

# Get the clone URL for the project
response=$(sagemaker-studio git get-clone-url --domain-id "$dataZoneDomainId" --project-id "$dataZoneProjectId" --profile DomainExecutionRoleCreds)
cloneUrl=$(echo "$response" | jq -r '.cloneUrl')
# Get the project default environment and extract the gitConnectionArn and gitBranchName
getProjectDefaultEnvResponse=$(sagemaker-studio project get-project-default-environment --domain-id "$dataZoneDomainId" --project-id "$dataZoneProjectId" --profile DomainExecutionRoleCreds)
gitConnectionArn=$(echo "$getProjectDefaultEnvResponse" | jq -r '.provisionedResources[] | select(.name=="gitConnectionArn") | .value')
gitBranchName=$(echo "$getProjectDefaultEnvResponse" | jq -r '.provisionedResources[] | select(.name=="gitBranchName") | .value')
dataZoneProjectRepositoryName=$(echo "$getProjectDefaultEnvResponse" | jq -r '.provisionedResources[] | select(.name=="codeRepositoryName") | .value')

 # Check if the cloneUrl is available
if [[ -n "$cloneUrl" ]]; then
    # Check if the cloneUrl contains "codeconnections" or "codestar-connections" (For customers created connection before Jun 7th)
    if [[ "$cloneUrl" == *"codeconnections"* ]] || [[ "$cloneUrl" == *"codestar-connections"* ]]; then
        # Check if the DomainExecutionRoleCreds profile exists in the AWS config file
        if grep -q 'DomainExecutionRoleCreds' /home/sagemaker-user/.aws/config; then
            /bin/bash /etc/sagemaker-ui/git_config.sh
            # Clone the repository using the cloneUrl and gitBranchName
            git clone "$cloneUrl" $DESTINATION_PATH -b "$gitBranchName"
        fi
    else
        # Clone the codeCommit repository
        clone_code_commit_repo "$dataZoneProjectRepositoryName"
    fi
else
    # If the cloneUrl is not available, check if the gitConnectionArn is available
    # If not available, clone codeCommit repository.
    [[ -z "$gitConnectionArn" ]] && clone_code_commit_repo "$dataZoneProjectRepositoryName"
fi
