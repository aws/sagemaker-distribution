ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN micromamba install -y --name base -c conda-forge pytest pytest-cov

RUN echo '#!/bin/bash' > /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo 'import_path=$(python -c "import sklearn; print(sklearn.__file__)")' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo 'sklearn_path=$(dirname "$import_path")' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo 'test_files=("test_base.py" "test_init.py")' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo 'for test_file in "${test_files[@]}"; do' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo '    echo "Running tests in $test_file"' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo '    pytest -v "$sklearn_path/tests/$test_file"' >> /home/sagemaker-user/run_scikit_learn_tests.sh && \
    echo 'done' >> /home/sagemaker-user/run_scikit_learn_tests.sh

RUN chmod +x /home/sagemaker-user/run_scikit_learn_tests.sh

WORKDIR /home/sagemaker-user

CMD ["./run_scikit_learn_tests.sh"]