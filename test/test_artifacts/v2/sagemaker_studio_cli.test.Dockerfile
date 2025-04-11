ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_studio_cli_test.sh .
RUN chmod +x run_sagemaker_studio_cli_test.sh
CMD ["./run_sagemaker_studio_cli_test.sh"]