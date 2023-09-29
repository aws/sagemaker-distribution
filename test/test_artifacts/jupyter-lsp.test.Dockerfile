ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE as base

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# TODO: How to do an existence check on TypeScript files?
