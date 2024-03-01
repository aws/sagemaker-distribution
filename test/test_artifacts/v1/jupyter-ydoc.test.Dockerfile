ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "from jupyter_ydoc import YBlob; yblob = YBlob(); assert yblob.get() == b''; yblob.set(b'012'); assert yblob.get() == b'012'"]