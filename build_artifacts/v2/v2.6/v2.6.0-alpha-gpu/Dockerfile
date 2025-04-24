FROM 700843992353.dkr.ecr.us-east-1.amazonaws.com/sagemaker-distribution-staging-repository@sha256:43b4a3af19ba16df3df3298ade0be6dae95c35f9c9454ba1d37bb7b7e6b29b5e

ENV MAMBA_USER="sagemaker-user"
USER $MAMBA_USER

COPY sagemaker_ui_post_startup.sh /etc/sagemaker-ui/
RUN micromamba install -y --name base -c conda-forge "amazon-sagemaker-jupyter-ai-q-developer=1.2.4" "jupyter-ai=2.31.1"

