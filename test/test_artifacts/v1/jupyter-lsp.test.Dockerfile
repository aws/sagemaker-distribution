ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import jupyter_lsp"]
CMD ["python", "-c", "import jupyterlab_lsp"]
