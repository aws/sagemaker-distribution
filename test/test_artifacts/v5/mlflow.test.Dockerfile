ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import mlflow"

RUN git clone --recursive https://github.com/mlflow/mlflow.git && \
    :
ENV XLA_FLAGS=--xla_gpu_cuda_data_dir=/opt/conda
WORKDIR "mlflow/"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_mlflow_tests.sh .
RUN chmod +x run_mlflow_tests.sh

# Run tests in run_mlflow_tests.sh
CMD ["./run_mlflow_tests.sh"]
