ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER ./pyhive .
RUN chmod +x ./pyhive.sh

RUN micromamba install -y --freeze-installed -c conda-forge papermill

CMD ["./pyhive.sh"]
