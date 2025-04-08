ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1


CMD ["python", "-c", "import sagemaker_studio; from sagemaker_studio import Project, Domain, ClientConfig;"]