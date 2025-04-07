ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN sudo apt-get update && \
    sudo apt-get install -y git

RUN git clone https://github.com/jupyter-widgets/ipywidgets.git

WORKDIR "ipywidgets"

RUN pip install jupyter nbconvert

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_ipywidgets_tests.sh ./
RUN chmod +x run_ipywidgets_tests.sh

CMD ["./run_ipywidgets_tests.sh"]
