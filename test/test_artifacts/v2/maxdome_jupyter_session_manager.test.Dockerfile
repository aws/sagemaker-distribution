ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Test import for current stage
# TODO: update the test to run unit tests of the package when available
CMD ["python", "-c", "import maxdome_jupyter_session_manager.maxdome_session_manager"]
