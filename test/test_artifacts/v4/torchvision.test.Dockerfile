ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/pytorch/vision 

WORKDIR "vision"

RUN micromamba install -y -c conda-forge pytest

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_torchvision_tests.sh .
RUN chmod +x run_torchvision_tests.sh
CMD ["./run_torchvision_tests.sh"]

