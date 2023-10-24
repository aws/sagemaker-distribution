ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER aws-glue-sessions/ .
RUN chmod +x run_glue_sessions_notebook.sh

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./run_glue_sessions_notebook.sh"]
