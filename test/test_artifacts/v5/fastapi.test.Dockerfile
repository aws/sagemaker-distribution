ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/fastapi/fastapi

WORKDIR "fastapi"

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_fastapi_tests.sh .

RUN chmod +x run_fastapi_tests.sh

CMD ["./run_fastapi_tests.sh"]

