from __future__ import absolute_import

import logging.config

SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER = "sagemaker_distribution.inference_server"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        SAGEMAKER_DISTRIBUTION_INFERENCE_LOGGER: {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
        "tornado.application": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
        "tornado.general": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
        "tornado.access": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
