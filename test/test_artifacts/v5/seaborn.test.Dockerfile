ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/mwaskom/seaborn.git

WORKDIR "seaborn"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_seaborn_tests.sh .
RUN chmod +x run_seaborn_tests.sh
CMD ["./run_seaborn_tests.sh"]
