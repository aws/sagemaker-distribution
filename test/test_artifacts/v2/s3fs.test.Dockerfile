ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/fsspec/s3fs.git

WORKDIR "s3fs"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_s3fs_tests.sh .
RUN chmod +x run_s3fs_tests.sh
CMD ["./run_s3fs_tests.sh"]
