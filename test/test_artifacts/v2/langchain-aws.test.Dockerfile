ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git

RUN git clone https://github.com/langchain-ai/langchain-aws /tmp/langchain-aws

CMD ["python", "-c", "import langchain_aws"]
CMD ["python", "-c", "from langchain_aws import BedrockLLM"]
CMD ["python", "-c", "from langchain_aws import ChatBedrock"]
CMD ["python", "-c", "from langchain_aws import SagemakerEndpoint"]
CMD ["python", "-c", "from langchain_aws import AmazonKendraRetriever"]
CMD ["python", "-c", "from langchain_aws import AmazonKnowledgeBasesRetriever"]
CMD ["python", "-c", "from langchain_aws import NeptuneAnalyticsGraph"]
CMD ["python", "-c", "from langchain_aws import NeptuneGraph"]


WORKDIR "/tmp/langchain-aws"

RUN pip install jupyter nbconvert

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_langchain_aws_tests.sh ./
RUN chmod +x run_langchain_aws_tests.sh

CMD ["./run_langchain_aws_tests.sh"]
