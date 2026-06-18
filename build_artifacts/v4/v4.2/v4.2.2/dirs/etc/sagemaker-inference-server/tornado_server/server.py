from __future__ import absolute_import

import asyncio
import importlib
import logging
import subprocess
import sys
from pathlib import Path

from utils.environment import Environment
from utils.exception import (
    InferenceCodeLoadException,
    RequirementsInstallException,
    ServerStartException,
)
from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class TornadoServer:
    """Holds serving logic using the Tornado framework.

    The serve.py script will invoke TornadoServer.serve() to start the serving process.
    The TornadoServer will install the runtime requirements specified through a requirements file.
    It will then load an handler function within an inference script and then front it will an /invocations
    route using the Tornado framework.
    """

    def __init__(self):
        """Initialize the serving behaviors.

        Defines the serving behavior through Environment() and locate where
        the inference code is contained.
        """

        self._environment = Environment()
        logger.setLevel(int(self._environment.logging_level))
        logger.debug(f"Environment: {str(self._environment)}")

        self._path_to_inference_code = (
            Path(self._environment.base_directory).joinpath(self._environment.code_directory)
            if self._environment.code_directory
            else Path(self._environment.base_directory)
        )
        logger.debug(f"Path to inference code: `{str(self._path_to_inference_code)}`")

    def initialize(self):
        """Initialize the serving artifacts and dependencies.

        Install the runtime requirements and then locate the handler function from
        the inference script.
        """

        logger.info("Initializing inference server...")
        self._install_runtime_requirements()
        self._handler = self._load_inference_handler()

    def serve(self):
        """Orchestrate the initialization and server startup behavior.

        Call the initalize() method, determine the right Tornado serving behavior (async or sync),
        and then start the Tornado server through asyncio
        """

        logger.info("Serving inference requests using Tornado...")
        self.initialize()

        if asyncio.iscoroutinefunction(self._handler):
            import async_handler as inference_handler
        else:
            import sync_handler as inference_handler

        try:
            asyncio.run(inference_handler.handle(self._handler, self._environment))
        except Exception as e:
            raise ServerStartException(e)

    def _install_runtime_requirements(self):
        """Install the runtime requirements."""

        logger.info("Installing runtime requirements...")
        requirements_txt = self._path_to_inference_code.joinpath(self._environment.requirements)
        if requirements_txt.is_file():
            try:
                subprocess.check_call(["micromamba", "install", "--yes", "--file", str(requirements_txt)])
            except Exception as e:
                logger.error(
                    "Failed to install requirements using `micromamba install`. Falling back to `pip install`..."
                )
                try:
                    subprocess.check_call(["pip", "install", "-r", str(requirements_txt)])
                except Exception as e:
                    raise RequirementsInstallException(e)
        else:
            logger.debug(f"No requirements file was found at `{str(requirements_txt)}`")

    def _load_inference_handler(self) -> callable:
        """Load the handler function from the inference script."""

        logger.info("Loading inference handler...")
        inference_module_name, handle_name = self._environment.code.split(".")
        if inference_module_name and handle_name:
            inference_module_file = f"{inference_module_name}.py"
            module_spec = importlib.util.spec_from_file_location(
                inference_module_file, str(self._path_to_inference_code.joinpath(inference_module_file))
            )
            if module_spec:
                sys.path.insert(0, str(self._path_to_inference_code.resolve()))
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)

                if hasattr(module, handle_name):
                    handler = getattr(module, handle_name)
                else:
                    raise InferenceCodeLoadException(
                        f"Handler `{handle_name}` could not be found in module `{inference_module_file}`"
                    )
                logger.debug(f"Loaded handler `{handle_name}` from module `{inference_module_name}`")
                return handler
            else:
                raise InferenceCodeLoadException(
                    f"Inference code could not be found at `{str(self._path_to_inference_code.joinpath(inference_module_file))}`"
                )
        raise InferenceCodeLoadException(
            f"Inference code expected in the format of `<module>.<handler>` but was provided as {self._environment.code}"
        )
