ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/jupyter-server/jupyter-scheduler

WORKDIR "jupyter-scheduler"

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_jupyter_scheduler_tests.sh .

RUN chmod +x run_jupyter_scheduler_tests.sh

CMD ["./run_jupyter_scheduler_tests.sh"]

