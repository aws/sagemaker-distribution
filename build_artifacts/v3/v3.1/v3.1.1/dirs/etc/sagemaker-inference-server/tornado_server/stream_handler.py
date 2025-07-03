from __future__ import absolute_import

import logging
from typing import AsyncIterator, Iterator

from tornado.ioloop import IOLoop

from utils.logger import SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER

logger = logging.getLogger(SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER)


class StreamHandler:
    """Mixin that enables async and sync streaming capabilities to the async and sync handlers

    stream() runs a provided iterator/generator fn in an async manner.
    astream() runs a provided async iterator/generator fn in an async manner.
    """

    async def stream(self, iterator: Iterator):
        """Streams the response from a sync response iterator

        A sync iterator must be manually iterated through asynchronously.
        In a loop, iterate through each next(iterator) call in an async execution.
        """

        self._set_stream_headers()

        while True:
            try:
                chunk = await IOLoop.current().run_in_executor(None, next, iterator)
                # Some iterators do not throw a StopIteration upon exhaustion.
                # Instead, they return an empty response. Account for this case.
                if not chunk:
                    raise StopIteration()

                self.write(chunk)
                await self.flush()
            except StopIteration:
                break
            except Exception as e:
                logger.error("Unexpected exception occurred when streaming response...")
                break

    async def astream(self, aiterator: AsyncIterator):
        """Streams the response from an async response iterator"""

        self._set_stream_headers()

        async for chunk in aiterator:
            self.write(chunk)
            await self.flush()

    def _set_stream_headers(self):
        """Set the headers in preparation for the streamed response"""

        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
