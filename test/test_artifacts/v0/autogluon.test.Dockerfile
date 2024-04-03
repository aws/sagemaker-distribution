ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE as base

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba install --freeze-installed -y conda-forge::pytest conda-forge::jupyter

RUN git clone --recursive https://github.com/autogluon/autogluon.git

WORKDIR "autogluon"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_autogluon_tests.sh .
RUN chmod +x run_autogluon_tests.sh
CMD ["./run_autogluon_tests.sh"]
