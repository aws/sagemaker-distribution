ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN micromamba install -y --name base -c conda-forge pytest pytest-cov parameterized && \
    pip install k5test

# run tests in the home directory
RUN echo '#!/bin/bash' > /home/sagemaker-user/run_python_gssapi_tests.sh && \
    echo 'import_path=$(python -c "import gssapi; print(gssapi.__file__)")' >> /home/sagemaker-user/run_python_gssapi_tests.sh && \
    echo 'gssapi_path=$(dirname "$import_path")' >> /home/sagemaker-user/run_python_gssapi_tests.sh && \
    echo 'pytest -v "$gssapi_path" "$@"' >> /home/sagemaker-user/run_python_gssapi_tests.sh

RUN chmod +x /home/sagemaker-user/run_python_gssapi_tests.sh

WORKDIR /home/sagemaker-user

CMD ["./run_python_gssapi_tests.sh"]
