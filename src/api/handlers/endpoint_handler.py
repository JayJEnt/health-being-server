from functools import wraps

from config import settings
from logger import configure_logger


logger = configure_logger()

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(f"Endpoint error: {ex}")
            return []
    return wrapper