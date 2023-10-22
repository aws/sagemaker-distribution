ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1


# Execute the unit tests for sagemaker-headless-execution-driver
CMD ["python", "-m", "unittest", "sagemaker_headless_execution_driver.test"]
