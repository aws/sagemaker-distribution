ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import jupyter_collaboration; import jupyter_server_fileid; from jupyter_ydoc import YBlob; yblob = YBlob(); assert yblob.get() == b''; yblob.set(b'012'); assert yblob.get() == b'012'"]
