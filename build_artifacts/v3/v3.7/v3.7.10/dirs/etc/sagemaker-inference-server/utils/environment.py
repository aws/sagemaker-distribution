from __future__ import absolute_import

import json
import os
from enum import Enum


class SageMakerInference(str, Enum):
    """Simple enum to define the mapping between dictionary key and environement variable."""

    BASE_DIRECTORY = "SAGEMAKER_INFERENCE_BASE_DIRECTORY"
    REQUIREMENTS = "SAGEMAKER_INFERENCE_REQUIREMENTS"
    CODE_DIRECTORY = "SAGEMAKER_INFERENCE_CODE_DIRECTORY"
    CODE = "SAGEMAKER_INFERENCE_CODE"
    LOG_LEVEL = "SAGEMAKER_INFERENCE_LOG_LEVEL"
    PORT = "SAGEMAKER_INFERENCE_PORT"


class Environment:
    """Retrieves and encapsulates SAGEMAKER_INFERENCE prefixed environment variables."""

    def __init__(self):
        """Initialize the environment variable mapping"""

        self._environment_variables = {
            SageMakerInference.BASE_DIRECTORY: "/opt/ml/model",
            SageMakerInference.REQUIREMENTS: "requirements.txt",
            SageMakerInference.CODE_DIRECTORY: os.getenv(SageMakerInference.CODE_DIRECTORY, None),
            SageMakerInference.CODE: os.getenv(SageMakerInference.CODE, "inference.handler"),
            SageMakerInference.LOG_LEVEL: os.getenv(SageMakerInference.LOG_LEVEL, 10),
            SageMakerInference.PORT: 8080,
        }

    def __str__(self):
        return json.dumps(self._environment_variables)

    @property
    def base_directory(self):
        return self._environment_variables.get(SageMakerInference.BASE_DIRECTORY)

    @property
    def requirements(self):
        return self._environment_variables.get(SageMakerInference.REQUIREMENTS)

    @property
    def code_directory(self):
        return self._environment_variables.get(SageMakerInference.CODE_DIRECTORY)

    @property
    def code(self):
        return self._environment_variables.get(SageMakerInference.CODE)

    @property
    def logging_level(self):
        return self._environment_variables.get(SageMakerInference.LOG_LEVEL)

    @property
    def port(self):
        return self._environment_variables.get(SageMakerInference.PORT)
