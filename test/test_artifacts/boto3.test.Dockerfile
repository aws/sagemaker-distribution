ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN sudo apt-get update && sudo apt-get install -y git && \
    git clone --recursive https://github.com/boto/boto3.git && \
    :

# For Running boto3 tests, we need pytest
RUN micromamba install -y conda-forge::pytest


WORKDIR "boto3"
COPY --chown=$MAMBA_USER:$MAMBA_USER run_boto3_tests.sh .
RUN chmod +x run_boto3_tests.sh
CMD ["./run_boto3_tests.sh"]
