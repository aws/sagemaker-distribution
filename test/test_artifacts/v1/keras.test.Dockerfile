ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && sudo apt-get install -y git graphviz && \
    git clone --recursive https://github.com/keras-team/keras-io.git && \
    :

# Some of the keras guides requires pydot and graphviz to be installed
RUN micromamba install -y --freeze-installed conda-forge::pydot "nvidia::cuda-nvcc>=11.8,<11.9" jax
ENV XLA_FLAGS=--xla_gpu_cuda_data_dir=/opt/conda

WORKDIR "keras-io/guides"

# Checkout a specific commit known to be compatible with the runtime's current version of TensorFlow.
# keras-io made backwards incompatible changes that broke these tests. Pinning at this commit for now
# at least until the runtime's TensorFlow dependency is upgraded to the next minor version
RUN git checkout 861b59747b43ce326bb0a12384a07d6632249901

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_keras_tests.sh .
RUN chmod +x run_keras_tests.sh
# Run tests in run_keras_tests.sh
CMD ["./run_keras_tests.sh"]
