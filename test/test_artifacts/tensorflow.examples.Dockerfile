ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/tensorflow/docs.git && \
    :

WORKDIR "docs/site/en/guide"
COPY --chown=$MAMBA_USER:$MAMBA_USER ./tensorflow/ ./
RUN chmod +x run_tensorflow_example_notebooks.sh

RUN pip install papermill

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "./run_tensorflow_example_notebooks.sh"]
