FROM 700843992353.dkr.ecr.us-east-1.amazonaws.com/sagemaker-distribution-staging-repository@sha256:f72dd98369557b3235f8982a841e4c8439af370b901cb2d19ff7f5d60de24aa3

ENV MAMBA_USER="sagemaker-user"
USER $MAMBA_USER

COPY sagemaker_ui_post_startup.sh /etc/sagemaker-ui/
RUN micromamba install -y --name base -c conda-forge "amazon-sagemaker-jupyter-ai-q-developer=1.2.4" "jupyter-ai=2.31.1"

