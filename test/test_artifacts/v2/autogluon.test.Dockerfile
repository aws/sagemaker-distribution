ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE as base

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba install --freeze-installed -y -c conda-forge pytest

RUN git clone --recursive https://github.com/autogluon/autogluon.git

WORKDIR "autogluon"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_autogluon_tests.sh .
RUN chmod +x run_autogluon_tests.sh
CMD ["./run_autogluon_tests.sh"]
