ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import amazon_sagemaker_sql_editor"]
