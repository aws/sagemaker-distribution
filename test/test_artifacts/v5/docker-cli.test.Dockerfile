ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_docker_cli_tests.sh ./
RUN chmod +x run_docker_cli_tests.sh

CMD ["./run_docker_cli_tests.sh"]