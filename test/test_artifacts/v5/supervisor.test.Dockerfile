ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git

RUN git clone https://github.com/Supervisor/supervisor.git 

WORKDIR "supervisor"

RUN micromamba install --freeze-installed -y -c conda-forge pytest

RUN pip install -e .

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_supervisor_tests.sh .

RUN chmod +x run_supervisor_tests.sh

CMD ["./run_supervisor_tests.sh"]
