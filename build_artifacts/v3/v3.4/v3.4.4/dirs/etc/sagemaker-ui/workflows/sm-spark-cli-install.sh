#!/bin/bash

# install sm-spark-cli
sudo curl -LO https://github.com/aws-samples/amazon-sagemaker-spark-ui/releases/download/v0.9.1/amazon-sagemaker-spark-ui.tar.gz && \
sudo tar -xvzf amazon-sagemaker-spark-ui.tar.gz && \
sudo chmod +x amazon-sagemaker-spark-ui/install-scripts/studio/install-history-server.sh && \
sudo amazon-sagemaker-spark-ui/install-scripts/studio/install-history-server.sh && \
rm -rf ~/.m2 && \
sudo rm -rf amazon-sagemaker-spark-ui*