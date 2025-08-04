"""/oauth2_google endpoint"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx

from api.handlers.exceptions import RescourceNotFound
from api.routers.oauth2_our import create_user
from api.routers.users_email_email import get_user_by_email
from api.schemas.user import User, UserBaseModel
from config import settings
from logger import logger


router = APIRouter(prefix="/oauth2_google", tags=["oauth2_google"])


@router.get("/login")
def login():
    if not all([settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET, settings.GOOGLE_REDIRECT_URI]):
        raise RuntimeError("Missing required Google OAuth environment variables")
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

@router.get("/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=404, detail="Authorization code not found")

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
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        user_response = await client.get(
            settings.GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        user = user_response.json()

        try:
            user_found_dict = await get_user_by_email(user["email"])
            user = User(**user_found_dict)
            logger.info(f'Successfully loged {user.email} in.')
        except RescourceNotFound:
            logger.info(
                f"Email: {user['email']} is not registered."
                f"Starting registeration process..."
            )
            user_creat_dict = {
                "username": user["name"],
                "email": user["email"]
            }
            user_create = UserBaseModel(**user_creat_dict)
            user: User = await create_user(user_create, other_provider=True)

        return user