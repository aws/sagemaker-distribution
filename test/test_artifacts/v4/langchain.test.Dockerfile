ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV OPENBLAS_NUM_THREADS=1

RUN micromamba install -y -c conda-forge pytest

# Create the test script
RUN echo '#!/bin/bash' > /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'set -e' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'echo "Langchain version: $(python -c "import langchain; print(langchain.__version__)")"' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'langchain_path=$(python -c "import langchain; import os; print(os.path.dirname(langchain.__file__))")' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'test_path="${langchain_path}/tests/unit_tests"' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'if [ -d "$test_path" ]; then' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo '    pytest "$test_path" -v' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'else' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo '    echo "Unit tests directory not found at $test_path"' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo '    echo "Available files in langchain directory:"' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo '    find "$langchain_path" -name "*.py"' >> /home/sagemaker-user/run_langchain_tests.sh && \
    echo 'fi' >> /home/sagemaker-user/run_langchain_tests.sh

RUN chmod +x /home/sagemaker-user/run_langchain_tests.sh

WORKDIR /home/sagemaker-user

CMD ["./run_langchain_tests.sh"]