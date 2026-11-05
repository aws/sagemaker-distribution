ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import mcp"

RUN git clone --recursive https://github.com/modelcontextprotocol/python-sdk.git && \
    :
RUN micromamba install --freeze-installed -y pyright pytest uv ruff trio pytest-flakefinder pytest-xdist pytest-pretty inline-snapshot dirty-equals
WORKDIR "python-sdk/"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_mcp_tests.sh .
RUN chmod +x run_mcp_tests.sh

# Run tests in run_mcp_tests.sh
CMD ["./run_mcp_tests.sh"]
