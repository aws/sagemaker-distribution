#!/bin/bash
RESOURCE_METADATA_FILE=/opt/ml/metadata/resource-metadata.json
DZ_DOMAIN_ID=$(jq -r '.AdditionalMetadata.DataZoneDomainId' < $RESOURCE_METADATA_FILE)
DZ_PROJECT_ID=$(jq -r '.AdditionalMetadata.DataZoneProjectId' < $RESOURCE_METADATA_FILE)
DZ_DOMAIN_REGION=$(jq -r '.AdditionalMetadata.DataZoneDomainRegion' < $RESOURCE_METADATA_FILE)
DZ_ENDPOINT=$(jq -r '.AdditionalMetadata.DataZoneEndpoint' < $RESOURCE_METADATA_FILE)

# install sm-spark-cli if workflows blueprint is enabled
if  [ "$(python /etc/sagemaker-ui/workflows/workflow_client.py check-blueprint --region "$DZ_DOMAIN_REGION" --domain-id "$DZ_DOMAIN_ID" --endpoint "$DZ_ENDPOINT" --project-id "$DZ_PROJECT_ID")" = "True" ]; then
    echo "Workflows blueprint is enabled. Installing sm-spark-cli."
    # install sm-spark-cli
    sudo curl -LO https://github.com/aws-samples/amazon-sagemaker-spark-ui/releases/download/v0.9.1/amazon-sagemaker-spark-ui.tar.gz && \
    sudo tar -xvzf amazon-sagemaker-spark-ui.tar.gz && \
    sudo chmod +x amazon-sagemaker-spark-ui/install-scripts/studio/install-history-server.sh && \
    sudo amazon-sagemaker-spark-ui/install-scripts/studio/install-history-server.sh && \
    rm -rf ~/.m2 && \
    sudo rm -rf amazon-sagemaker-spark-ui*
fi