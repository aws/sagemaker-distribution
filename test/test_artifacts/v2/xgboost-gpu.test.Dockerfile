ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/dmlc/xgboost

WORKDIR "xgboost"

RUN micromamba install --freeze-installed -y -c conda-forge xgboost hypothesis loky pytest pytest-timeout 

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_xgboost_gpu_tests.sh .

RUN chmod +x run_xgboost_gpu_tests.sh

CMD ["./run_xgboost_gpu_tests.sh"]
