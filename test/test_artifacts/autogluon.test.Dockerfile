ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE as base

ARG MAMBA_DOCKERFILE_ACTIVATE=1
ARG AUTOGLUON_VERSION="0.8.2"

RUN sudo apt-get update && sudo apt-get install -y git graphviz graphviz-dev

# TODO: remove autogluon.tabular once it's included into the distribution
RUN micromamba install -y conda-forge::pytest conda-forge::pygraphviz conda-forge::jupyter conda-forge::nbconvert conda-forge::autogluon==$AUTOGLUON_VERSION

RUN git clone --recursive https://github.com/autogluon/autogluon.git

WORKDIR "autogluon"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_autogluon_tests.sh .
RUN chmod +x run_autogluon_tests.sh
CMD ["./run_autogluon_tests.sh"]
