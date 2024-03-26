ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Test that the toolkit helper can run
# TODO: update to test full functionality
CMD ["maxdome-toolkit", "connection", "--help"]
