ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1


# Execute execution_driver module to for sagemaker-headless-execution-driver installation
CMD ["python", "-c",  "import sagemaker_headless_execution_driver.headless_execution as execution_driver"]