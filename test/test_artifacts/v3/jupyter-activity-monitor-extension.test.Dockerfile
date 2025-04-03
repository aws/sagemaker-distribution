ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install pytest --freeze-installed --yes --channel conda-forge --name base
RUN micromamba install pytest-jupyter --freeze-installed --yes --channel conda-forge --name base
RUN SITE_PACKAGES=$(pip show jupyter-activity-monitor-extension | grep Location | awk '{print $2}') && \
    cd "$SITE_PACKAGES/jupyter_activity_monitor_extension/tests/" && pytest -p pytest_jupyter.jupyter_server
