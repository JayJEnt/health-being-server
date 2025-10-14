from datetime import timedelta

from api.authentication.token import create_access_token, get_payload_from_token
from api.crud.single_entity.get_methods import get_element_by_name
from email_postman.email_postman import email_postman
from email_postman.templates import VERIFICATION_TEMPLATE
from api.handlers.http_exceptions import InvalidToken, ResourceNotFound
from config import settings


async def create_email_verification_token(email: str, expire_time: int) -> str:
    data = {"sub": email, "type": "email_verification"}
    expire = timedelta(minutes=expire_time)
    return create_access_token(data, expire)


async def send_verification_email(email: str) -> dict:
    expire_time = settings.MAIL_EXPIRE_TIME
    token = await create_email_verification_token(email, expire_time)
    verification_link = f"{settings.MAIL_FRONTEND_CALLBACK}?token={token}"

    subject = VERIFICATION_TEMPLATE.get("subject")
    html_body = VERIFICATION_TEMPLATE.get("body").format(
        verification_link=verification_link, expire_time=expire_time
    )

    message = email_postman.create_message(email, subject, html_body)
    email_postman.send_message(message)

    return {"message": f"Verification email sent to {email}"}


async def verify_email_token(token: str) -> bool:
    payload = await get_payload_from_token(token)
    email = payload.get("sub", None)
    if not email or payload.get("type") != "email_verification":
        raise InvalidToken

    try:
        await get_element_by_name("user", email, alternative_name=True)
    except ResourceNotFound:
        return False

    return True
