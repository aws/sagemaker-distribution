ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN python -c "import sagemaker-gen-ai-jupyterlab-extension"

RUN micromamba install --freeze-installed -y pyright pytest uv ruff trio pytest-flakefinder pytest-xdist pytest-pretty inline-snapshot dirty-equals
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_gen_ai_jupyterlab_extension.sh .
RUN chmod +x run_sagemaker_gen_ai_jupyterlab_extension.sh

# Run tests in run_sagemaker_gen_ai_jupyterlab_extension.sh
CMD ["./run_sagemaker_gen_ai_jupyterlab_extension.sh"]