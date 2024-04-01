ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER ./sagemaker-studio-analytics-extension .
RUN chmod +x ./sagemaker-studio-analytics-extension.sh

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./sagemaker-studio-analytics-extension.sh"]
