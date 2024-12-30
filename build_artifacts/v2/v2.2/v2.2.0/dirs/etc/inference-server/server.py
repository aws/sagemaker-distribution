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
    ServerStartException
)
from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class TornadoServer:
    def serve(self):
        if asyncio.iscoroutinefunction(self._handler):
            logger.info("Starting inference server in asynchronous mode...")
            import tornado_server.async_server as inference_server
        else:
            logger.info("Starting inference server in synchronous mode...")
            import tornado_server.sync_server as inference_server

        try:
            asyncio.run(inference_server.serve(self._handler, self._environment))
        except Exception as e:
            raise ServerStartException(e)


class InferenceServer(TornadoServer):
    def __init__(self):
        self._environment = Environment()
        logger.setLevel(self._environment.logging_level)
        logger.debug(f"Environment: {str(self._environment)}")

        self._path_to_inference_code = (
            Path(self._environment.base_directory).joinpath(self._environment.code_directory)
            if self._environment.code_directory else
            Path(self._environment.base_directory)
        )
        logger.debug(f"Path to inference code: `{str(self._path_to_inference_code)}`")

        self._handler = None

    def initialize(self):
        self._install_runtime_requirements()
        self._handler = self._load_inference_handler()

    def _install_runtime_requirements(self):
        logger.info("Installing runtime requirements...")
        
        requirements_txt = self._path_to_inference_code.joinpath(self._environment.requirements)
        if requirements_txt.is_file():
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_txt)]
                )
            except Exception as e:
                raise RequirementsInstallException(e)
        else:
            logger.debug(f"No requirements file was found at `{str(requirements_txt)}`")

    def _load_inference_handler(self) -> callable:
        logger.info("Loading inference handler...")

        inference_module_name, handle_name = self._environment.code.split(".")
        if inference_module_name and handle_name:
            inference_module_file = f"{inference_module_name}.py"
            module_spec = importlib.util.spec_from_file_location(
                inference_module_file,
                str(self._path_to_inference_code.joinpath(inference_module_file))
            )
            if module_spec:
                sys.path.insert(0, str(self._path_to_inference_code.resolve()))
                inference_module = module_spec.loader.load_module(inference_module_file)
                if hasattr(inference_module, handle_name):
                    handler = getattr(inference_module, handle_name)
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
            f"Inference code expected in the format of `<module>.<handler>` but was provided as {code}"
        )


if __name__ == "__main__":
    inference_server = InferenceServer()
    inference_server.initialize()
    inference_server.serve()
