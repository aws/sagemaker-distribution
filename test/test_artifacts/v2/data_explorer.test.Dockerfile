ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --freeze-installed -c conda-forge pytest-jupyter

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_data_explorer_test.sh .
RUN chmod +x run_data_explorer_test.sh
CMD ["./run_data_explorer_test.sh"]
