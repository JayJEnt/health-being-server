import random

from api.email_postman.email_postman import email_postman
from api.email_postman.templates import VERIFICATION_TEMPLATE


async def send_email_verification(email: str):
    otp = "".join([str(random.randint(0, 9)) for i in range(6)])
    expire_time = 10
    subject = VERIFICATION_TEMPLATE.get("subject")
    html_body = VERIFICATION_TEMPLATE.get("body").format(
        otp=otp, expire_time=expire_time
    )

    message = email_postman.create_message(email, subject, html_body)
    email_postman.send_message(message)

    return {"message": f"Test email have been send properly with otp: {otp}"}


async def email_authentication(otp: str):
    pass
