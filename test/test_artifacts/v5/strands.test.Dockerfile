ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import strands"

RUN git clone --recursive https://github.com/strands-agents/sdk-python.git && \
    :
RUN micromamba install --freeze-installed -y pyright pytest uv ruff trio pytest-flakefinder pytest-xdist pytest-pretty inline-snapshot dirty-equals
WORKDIR "sdk-python/"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_strands_tests.sh .
RUN chmod +x run_strands_tests.sh

# Run tests in run_strands_tests.sh
CMD ["./run_strands_tests.sh"]