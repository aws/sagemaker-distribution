ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import sagemaker_mlflow"

RUN sudo apt-get update && sudo apt-get install -y git && \
    git clone --recursive https://github.com/aws/sagemaker-mlflow.git && \
    :

# For running sagemaker-mlflow tests, we need pytest
RUN micromamba install -y --freeze-installed -c conda-forge pytest

WORKDIR "sagemaker-mlflow/"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_mlflow_tests.sh .
RUN chmod +x run_sagemaker_mlflow_tests.sh
# Run tests in run_matplotlib_tests.sh
CMD ["./run_sagemaker_mlflow_tests.sh"]
