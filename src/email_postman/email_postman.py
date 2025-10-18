from email.message import EmailMessage
from functools import wraps
from smtplib import SMTP

from api.handlers.http_exceptions import InternalServerError
from config import settings
from logger import logger


class EmailPostman:
    def __init__(self):
        self._server = SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        self._server.starttls()
        try:
            self._server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        except Exception as ex:
            logger.error(f"EmailPostman connection error: {ex}")
            raise ConnectionRefusedError

    @staticmethod
    def error_handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Processing request: {func.__name__}")
                result = func(*args, **kwargs)
                logger.info("Sucesfully processed.")
                return result
            except Exception as ex:
                logger.error(f"EmailPostman error: {ex}")
                raise InternalServerError

        return wrapper

    @staticmethod
    @error_handler
    def create_message(email: str, subject: str, body: str) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.MAIL_FROM
        message["To"] = email
        message.add_alternative(body, subtype="html")

        return message

    @error_handler
    def send_message(self, message: EmailMessage) -> None:
        self._server.send_message(message)


email_postman = EmailPostman()
