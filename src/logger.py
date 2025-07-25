from loguru import logger

import sys

from config import settings


def configure_logger():
    """Configure the logger based on the environment settings."""
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<level>{level: <8}</level> <yellow>{name}</yellow>:<yellow>{function}</yellow>:<yellow>{line}</yellow> - <level>{message}</level>",
        )

    return logger