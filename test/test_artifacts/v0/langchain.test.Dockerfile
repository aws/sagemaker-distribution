ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "from langchain.llms import Bedrock; tests_succeeded = 0 if Bedrock else 1; sys.exit(tests_succeeded)"]
