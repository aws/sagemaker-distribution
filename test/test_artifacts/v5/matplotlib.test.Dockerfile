ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN sudo apt-get update && sudo apt-get install -y git && \
    git clone --recursive https://github.com/matplotlib/matplotlib.git && \
    :

# TODO: Come up with a different way to test matplotlib installation.
# Currently we will be running all the python files in galleries/tutorials
# But this directory structure might change in the future. In the past, "galleries/tutorials"
# didn't exist. Previously the repository just had a "tutorials" folder.
WORKDIR "matplotlib/galleries/tutorials"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_matplotlib_tests.sh .
RUN chmod +x run_matplotlib_tests.sh
# Run tests in run_matplotlib_tests.sh
CMD ["./run_matplotlib_tests.sh"]
