ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN micromamba install -y --name base -c conda-forge pytest pytest-cov

RUN echo '#!/bin/bash' > /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'set -e' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'import_path=$(python -c "import tf_keras; print(tf_keras.__file__)")' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'tf_keras_path=$(dirname "$import_path")' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'echo "tf-keras path: $tf_keras_path"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'test_file="keras_doctest.py"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'test_path=$(find "$tf_keras_path" -name "$test_file" -print -quit)' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'if [ -n "$test_path" ]; then' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    echo "Running test: $test_path"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    pytest -v "$test_path"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'else' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    echo "Test file not found: $test_file"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    echo "Available files in tf_keras:"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    find "$tf_keras_path" -name "*.py"' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo '    exit 1' >> /home/sagemaker-user/run_tf_keras_tests.sh && \
    echo 'fi' >> /home/sagemaker-user/run_tf_keras_tests.sh

RUN chmod +x /home/sagemaker-user/run_tf_keras_tests.sh

WORKDIR /home/sagemaker-user

CMD ["./run_tf_keras_tests.sh"]