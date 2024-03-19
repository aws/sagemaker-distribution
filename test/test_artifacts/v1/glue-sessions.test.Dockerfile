ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/run_glue_sessions_notebook.sh .
RUN chmod +x run_glue_sessions_notebook.sh
COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/glue_notebook.ipynb .
RUN chmod +x glue_notebook.ipynb

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./run_glue_sessions_notebook.sh"]
