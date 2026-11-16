ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import langchain_aws"]
CMD ["python", "-c", "from langchain_aws import BedrockLLM"]
CMD ["python", "-c", "from langchain_aws import ChatBedrock"]
CMD ["python", "-c", "from langchain_aws import SagemakerEndpoint"]
CMD ["python", "-c", "from langchain_aws import AmazonKendraRetriever"]
CMD ["python", "-c", "from langchain_aws import AmazonKnowledgeBasesRetriever"]
CMD ["python", "-c", "from langchain_aws import NeptuneAnalyticsGraph"]
CMD ["python", "-c", "from langchain_aws import NeptuneGraph"]
