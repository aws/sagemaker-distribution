ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_code_editor_tests.sh ./
RUN chmod +x run_sagemaker_code_editor_tests.sh

CMD ["./run_sagemaker_code_editor_tests.sh"]
