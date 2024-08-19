ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import mlflow"

RUN sudo apt-get update && sudo apt-get install -y git && \
    git clone --recursive https://github.com/mlflow/mlflow.git && \
    :

WORKDIR "mlflow/"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_mlflow_tests.sh .
RUN chmod +x run_mlflow_tests.sh
# Run tests in run_matplotlib_tests.sh
CMD ["./run_mlflow_tests.sh"]
