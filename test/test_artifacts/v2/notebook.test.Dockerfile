ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/jupyter/notebook

WORKDIR "notebook"

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_notebook_tests.sh .

RUN chmod +x run_notebook_tests.sh

CMD ["./run_notebook_tests.sh"]

