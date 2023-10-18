ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_glue_sessions_notebooks.sh .
RUN chmod +x run_glue_sessions_tests.sh
COPY --chown=$MAMBA_USER:$MAMBA_USER notebooks/glue_notebook.ipynb .
RUN chmod +x glue_notebook.ipynb

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./run_glue_sessions_notebook.sh"]
