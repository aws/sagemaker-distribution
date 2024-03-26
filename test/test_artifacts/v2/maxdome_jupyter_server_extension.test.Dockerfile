ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --freeze-installed -c conda-forge pytest-jupyter

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_maxdome_jupyter_server_extension_test.sh .
RUN chmod +x run_maxdome_jupyter_server_extension_test.sh
CMD ["./run_maxdome_jupyter_server_extension_test.sh"]
