ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN test -f /opt/conda/share/sagemaker_workflows/plugins/amzn_sagemaker_studio-*.whl || (echo "sagemaker studio (python sdk) wheel does not exist" && exit 1)
RUN test -f /opt/conda/share/sagemaker_workflows/plugins/amzn_SagemakerWorkflowsOperator-*.whl || (echo "sagemaker workflows operators wheel does not exist" && exit 1)
RUN test -f /opt/conda/share/sagemaker_workflows/requirements/requirements.txt || (echo "requirements.txt does not exist" && exit 1)
