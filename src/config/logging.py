import logging.config
from typing import Dict, Any

from src.utils.context_utils import RequestIdFilter

DEFAULT_LEVEL = "INFO"


def dict_config(level: str = DEFAULT_LEVEL) -> Dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {"()": RequestIdFilter}
        },
        "formatters": {
            "plain": {
                "format": "%(asctime)s %(levelname)s [%(name)s] %(request_id)s %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s %(levelname)s [%(name)s] %(request_id)s %(module)s:%(lineno)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "plain",
                "filters": ["request_id"],
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": level,
            "handlers": ["console"]
        },
        "loggers": {
            "uvicorn": {"level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"level": "INFO"},
            "sqlalchemy": {"level": "WARNING"},
            "sqlalchemy.engine": {"level": "INFO"},
            "aiokafka": {"level": "WARNING"},
            "asyncio": {"level": "WARNING"},
            "src": {"level": "DEBUG"},
        }
    }


def configure_logging(level: str = DEFAULT_LEVEL) -> None:
    cfg = dict_config(level)
    logging.config.dictConfig(cfg)
    logging.getLogger(__name__).debug("Logging configured (level=%s)", level)
