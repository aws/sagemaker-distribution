ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install pandas[test]

COPY --chown=$MAMBA_USER:$MAMBA_USER run_pandas_tests.py .
CMD ["python", "run_pandas_tests.py"]
