from __future__ import absolute_import

import asyncio
import logging
from typing import AsyncIterator, Iterator

import tornado.web
from stream_handler import StreamHandler

from utils.environment import Environment
from utils.exception import AsyncInvocationsException
from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class InvocationsHandler(tornado.web.RequestHandler, StreamHandler):
    """Handler mapped to the /invocations POST route.

    This handler wraps the async handler retrieved from the inference script
    and encapsulates it behind the post() method. The post() method is done
    asynchronously.
    """

    def initialize(self, handler: callable, environment: Environment):
        """Initializes the handler function and the serving environment."""

        self._handler = handler
        self._environment = environment

    async def post(self):
        """POST method used to encapsulate and invoke the async handle method asynchronously"""

        try:
            response = await self._handler(self.request)

            if isinstance(response, Iterator):
                await self.stream(response)
            elif isinstance(response, AsyncIterator):
                await self.astream(response)
            else:
                self.write(response)
        except Exception as e:
            raise AsyncInvocationsException(e)


class PingHandler(tornado.web.RequestHandler):
    """Handler mapped to the /ping GET route.

    Ping handler to monitor the health of the Tornados server.
    """

    def get(self):
        """Simple GET method to assess the health of the server."""

        self.write("")


async def handle(handler: callable, environment: Environment):
    """Serves the async handler function using Tornado.

    Opens the /invocations and /ping routes used by a SageMaker Endpoint
    for inference serving capabilities.
    """

    logger.info("Starting inference server in asynchronous mode...")

    app = tornado.web.Application(
        [
            (r"/invocations", InvocationsHandler, dict(handler=handler, environment=environment)),
            (r"/ping", PingHandler),
        ]
    )
    app.listen(environment.port)
    logger.debug(f"Asynchronous inference server listening on port: `{environment.port}`")
    await asyncio.Event().wait()
