ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

USER root
RUN mkdir -p /opt/ml/metadata
# Kernels need this json file to be present in the specific location
COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/resource-metadata.json /opt/ml/metadata/

COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/run_glue_sessions_notebook.sh .
RUN chmod +x run_glue_sessions_notebook.sh
COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/glue_notebook.ipynb .
RUN chmod +x glue_notebook.ipynb

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./run_glue_sessions_notebook.sh"]
