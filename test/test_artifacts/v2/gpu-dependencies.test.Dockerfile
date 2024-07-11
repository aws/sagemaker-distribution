ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Execute cuda valudaiton script:
# 1. Check if TensorFlow is installed with CUDA support for GPU image
# 2. Check if Pytorch is installed with CUDA support for GPU image
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/cuda_validation.py .
RUN chmod +x cuda_validation.py
RUN python3 cuda_validation.py