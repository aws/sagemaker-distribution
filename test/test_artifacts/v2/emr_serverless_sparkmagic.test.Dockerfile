ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Test import 
# TODO: update the test to run unit tests of the package when available
CMD ["python", "-c", "import emr_serverless_sparkmagic.customauthenticator"]
