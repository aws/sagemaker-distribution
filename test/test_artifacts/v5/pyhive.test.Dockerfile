ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/dropbox/PyHive.git

WORKDIR "PyHive"

RUN micromamba install --freeze-installed -y -c conda-forge pytest

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_pyhive_tests.sh .
RUN chmod +x run_pyhive_tests.sh

CMD ["./run_pyhive_tests.sh"]
