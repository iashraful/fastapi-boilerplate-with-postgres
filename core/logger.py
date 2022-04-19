from pydantic import BaseModel
from core.config import settings


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = settings.PROJECT_NAME
    LOG_FORMAT: str = settings.LOG_FORMAT
    LOG_LEVEL: str = settings.LOG_LEVEL

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        settings.PROJECT_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
