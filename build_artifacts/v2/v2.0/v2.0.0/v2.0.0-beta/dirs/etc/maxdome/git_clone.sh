#!/bin/bash
METADATA=/opt/ml/metadata/resource-metadata.json

# Extract the required fields from meta data stored in opt/ml/metadata.
dataZoneProjectRepositoryName=$(grep -o '"DataZoneProjectRepositoryName":"[^"]*"' "$METADATA" | cut -d ':' -f 2 | tr -d '"')

#User directory on which the user will have full access to . 
MD_USER="sagemaker-user"
USER_DIRECTORY="/home/${MD_USER}"

# Configuring git credential helper to use AWS creds when connecting to Codecommit Repo. 
git config --global credential.helper '!aws codecommit credential-helper $@' 
git config --global credential.UseHttpPath true

if  [ ! -d $USER_DIRECTORY/$dataZoneProjectRepositoryName ]; then
    git clone  https://git-codecommit.$AWS_REGION.amazonaws.com/v1/repos/$dataZoneProjectRepositoryName $USER_DIRECTORY/$dataZoneProjectRepositoryName 
    # if the above command exit with nonzero exit code ,delete the partially cloned Repo. 
    if [ $? -ne 0 ]; then 
        echo "Git clone of the Project repository has failed. Please refer to the documentation to understand how to fix this."
        if [ -d $USER_DIRECTORY/$dataZoneProjectRepositoryName ]; then
            rm -rf $USER_DIRECTORY/$dataZoneProjectRepositoryName
        fi
    fi

fi
