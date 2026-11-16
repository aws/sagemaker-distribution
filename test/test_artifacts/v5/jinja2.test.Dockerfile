ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN micromamba install -y -c conda-forge jinja2 

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_jinja2_tests.sh ./

RUN chmod +x run_jinja2_tests.sh

CMD ["./run_jinja2_tests.sh"]
