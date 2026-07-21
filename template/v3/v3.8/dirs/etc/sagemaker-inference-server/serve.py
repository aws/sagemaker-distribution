from __future__ import absolute_import

"""
TODO: when adding support for more serving frameworks, move the below logic into a condition statement.
We also need to define the right environment variable for signify what serving framework to use.

Ex.

inference_server = None
serving_framework = os.getenv("SAGEMAKER_INFERENCE_FRAMEWORK", None)

if serving_framework == "FastAPI":
    inference_server = FastApiServer()
elif serving_framework == "Flask":
    inference_server = FlaskServer()
else:
    inference_server = TornadoServer()

inference_server.serve()

"""
from tornado_server.server import TornadoServer

inference_server = TornadoServer()
inference_server.serve()
