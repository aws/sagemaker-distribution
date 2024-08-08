ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/aws/sagemaker-python-sdk.git

WORKDIR "sagemaker-python-sdk"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_pysdk_tests.sh .
RUN chmod +x run_pysdk_tests.sh
CMD ["./run_pysdk_tests.sh"]
