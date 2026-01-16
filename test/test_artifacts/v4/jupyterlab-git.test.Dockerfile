ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git 

RUN git clone --recursive https://github.com/jupyterlab/jupyterlab-git

WORKDIR "jupyterlab-git"

RUN micromamba install --freeze-installed -y -c conda-forge pytest

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_jupyterlab_git_tests.sh .
RUN chmod +x run_jupyterlab_git_tests.sh

CMD ["./run_jupyterlab_git_tests.sh"]
