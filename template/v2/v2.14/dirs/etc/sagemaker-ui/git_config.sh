#!/bin/bash
set -eux

sourceMetaData=/opt/ml/metadata/resource-metadata.json
dataZoneDomainRegion=$(jq -r '.AdditionalMetadata.DataZoneDomainRegion' < $sourceMetaData)

# Configure Git to use the AWS CodeCommit credential helper with profile DomainExecutionRoleCreds
git config --global credential.helper "!aws --profile DomainExecutionRoleCreds --region $dataZoneDomainRegion codecommit credential-helper --ignore-host-check $@"
git config --global credential.UseHttpPath true
