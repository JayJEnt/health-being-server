from fastapi import Request
from fastapi.responses import RedirectResponse
import httpx

from datetime import timedelta

from api.authentication.oauth2_our import register
from api.authentication.token import create_access_token
from api.crud.single_entity.get_methods import get_element_by_name
from api.handlers.http_exceptions import (
    ResourceNotFound,
    AuthorizationCodeNotFound,
    TokenNotRecived,
)
from api.handlers.custom_exceptions import MissingVariables
from api.schemas.user import User, UserBaseModel
from config import settings
from logger import logger


async def google_login():
    if not all(
        [
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            settings.GOOGLE_REDIRECT_URI,
        ]
    ):
        raise MissingVariables
    url = (
        f"{settings.GOOGLE_AUTH_ENDPOINT}?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    logger.debug(f"Full google authentication url with params:\n{url}")
    return RedirectResponse(url)


async def google_auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise AuthorizationCodeNotFound

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(settings.GOOGLE_TOKEN_ENDPOINT, data=data)
        token_data = token_response.json()
        access_token = token_data.get("access_token", "")

        if not access_token:
            raise TokenNotRecived

        user_response = await client.get(
            settings.GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        user = user_response.json()

        try:
            user_found_dict = await get_element_by_name(
                "user", user["email"], alternative_name=True
            )
            user = User(**user_found_dict)
            logger.info(f"Successfully loged {user.email} in.")
        except ResourceNotFound:
            logger.info(
                f"Email: {user['email']} is not registered."
                f"Starting registeration process..."
            )
            user_creat_dict = {"username": user["name"], "email": user["email"]}
            user_create = UserBaseModel(**user_creat_dict)
            user = User(**await register(user_create, other_provider=True))

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "provider": "google",
        }

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

        access_token = create_access_token(
            data=user_data, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
