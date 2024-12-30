from __future__ import absolute_import

import json
import os
from enum import Enum

class SageMakerInference(str, Enum):
    BASE_DIRECTORY = "SAGEMAKER_INFERENCE_BASE_DIRECTORY"
    REQUIREMENTS = "SAGEMAKER_INFERENCE_REQUIREMENTS"
    CODE_DIRECTORY = "SAGEMAKER_INFERENCE_CODE_DIRECTORY"
    CODE = "SAGEMAKER_INFERENCE_CODE"
    LOGGING_LEVEL = "SAGEMAKER_INFERENCE_LOGGING_LEVEL"
    PORT = "SAGEMAKER_INFERENCE_PORT"


class Environment:
    def __init__(self):
        self._environment_variables = {
            SageMakerInference.BASE_DIRECTORY: "/opt/ml/model",
            SageMakerInference.REQUIREMENTS: "requirements.txt",
            SageMakerInference.CODE_DIRECTORY: os.getenv(SageMakerInference.CODE_DIRECTORY, None),
            SageMakerInference.CODE: os.getenv(SageMakerInference.CODE, "inference.handler"),
            SageMakerInference.LOGGING_LEVEL: os.getenv(SageMakerInference.LOGGING_LEVEL, 10),
            SageMakerInference.PORT: os.getenv(SageMakerInference.PORT, 8080)
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
        return self._environment_variables.get(SageMakerInference.LOGGING_LEVEL)

    @property
    def port(self):
        return self._environment_variables.get(SageMakerInference.PORT)
