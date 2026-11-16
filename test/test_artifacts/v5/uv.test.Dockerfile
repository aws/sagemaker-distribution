ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN echo 'import requests; print(requests.get("https://astral.sh"))' > example.py

RUN uv add --script example.py requests
CMD uv run example.py