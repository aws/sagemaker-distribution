ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && sudo apt-get install -y git graphviz && \
    git clone --recursive https://github.com/keras-team/keras-io.git && \
    :

# Some of the keras guides requires pydot and graphviz to be installed
RUN micromamba install -y --freeze-installed -c conda-forge pydot cuda-nvcc jax
ENV XLA_FLAGS=--xla_gpu_cuda_data_dir=/opt/conda

WORKDIR "keras-io/guides"

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_keras_tests.sh .
RUN chmod +x run_keras_tests.sh
# Run tests in run_keras_tests.sh
CMD ["./run_keras_tests.sh"]
