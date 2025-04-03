ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/aws/sagemaker-python-sdk.git

RUN micromamba install -y --freeze-installed -c conda-forge pytest mock stopit awslogs

# Sagemaker Python SDK's unit tests requires AWS_DEFAULT_REGION to be set. So, using an arbitrary value of us-east-1
ENV AWS_DEFAULT_REGION=us-east-1
WORKDIR "sagemaker-python-sdk"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_pysdk_tests.sh .
RUN chmod +x run_pysdk_tests.sh
CMD ["./run_pysdk_tests.sh"]
