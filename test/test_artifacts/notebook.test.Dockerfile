ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE as base

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "from notebook import notebookapp; tests_succeeded = 0 if notebookapp else 1; sys.exit(tests_succeeded)"]
