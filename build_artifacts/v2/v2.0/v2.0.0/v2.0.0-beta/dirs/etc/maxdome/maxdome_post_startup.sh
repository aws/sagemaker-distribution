#!/bin/bash
sourceMetaData=/opt/ml/metadata/resource-metadata.json

# Extract the required fields from meta data stored in opt/ml/metadata.
dataZoneDomainId=$(grep -o '"DataZoneDomainId":"[^"]*"' "$sourceMetaData" | cut -d ':' -f 2 | tr -d '"')
dataZoneUserId=$(grep -o '"DataZoneUserId":"[^"]*"' "$sourceMetaData" | cut -d ':' -f 2 | tr -d '"')
dataZoneProjectRepositoryName=$(grep -o '"DataZoneProjectRepositoryName":"[^"]*"' "$sourceMetaData" | cut -d ':' -f 2 | tr -d '"')

# Run AWS CLI command to get the username from DataZone User Profile.
response=$( aws datazone get-user-profile --domain-identifier "$dataZoneDomainId" --user-identifier "$dataZoneUserId" --region "$AWS_REGION" )
username=$(echo "$response" | awk -F':' '/"username"/{print $2}' | tr -d '"'| xargs)

# Setting up the Git identity for the user . 
git config --global user.email "$username"
git config --global user.name "$username"

if  [ ! -d $HOME/$dataZoneProjectRepositoryName ]; then
    git clone  codecommit::$AWS_REGION://$dataZoneProjectRepositoryName $HOME/$dataZoneProjectRepositoryName 
    # if the above command exit with nonzero exit code ,delete the partially cloned Repo. 
    if [ $? -ne 0 ]; then 
        echo "Git clone of the Project repository has failed. Please refer to the documentation to understand how to fix this."
        if [ -d $HOME/$dataZoneProjectRepositoryName ]; then
            rm -rf $HOME/$dataZoneProjectRepositoryName
        fi
    fi
fi

