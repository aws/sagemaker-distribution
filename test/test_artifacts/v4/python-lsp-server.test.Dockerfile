ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/python-lsp/python-lsp-server

WORKDIR "python-lsp"

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_python_lsp_server_tests.sh .

RUN chmod +x run_python_lsp_server_tests.sh
