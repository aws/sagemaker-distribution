ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# "Confirm that installation succeeded" by running this - https://github.com/python-lsp/python-lsp-server#installation
CMD ["pylsp", "--help"]
