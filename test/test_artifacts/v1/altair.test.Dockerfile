ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import altair"]

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/altair-viz/altair_notebooks.git && \
    :

WORKDIR "altair_notebooks/notebooks"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_altair_example_notebooks.sh ./
RUN chmod +x run_altair_example_notebooks.sh

# Example notebooks' dependencies
RUN micromamba install -y --freeze-installed -c conda-forge papermill vega_datasets pandas matplotlib numpy

CMD ["./run_altair_example_notebooks.sh"]
