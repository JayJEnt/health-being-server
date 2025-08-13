import sys

from loguru import logger
from config import settings


def configure_logger():
    """Configure the logger based on the environment settings."""
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<level>{level: <8}</level> <yellow>{name}</yellow>:<yellow>{function}</yellow>:<yellow>{line}</yellow> - <level>{message}</level>",
        )

    return logger

logger = configure_logger()