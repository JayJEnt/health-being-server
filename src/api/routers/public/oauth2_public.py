"""/oauth2 router"""

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from api.authentication.oauth2_google import google_login, google_auth_callback
from api.authentication.oauth2_our import our_login, our_register
from api.authentication.email_authentication import (
    send_email_verification,
    email_authentication,
)
from api.handlers.http_exceptions import UnknownProvider
from api.schemas.user import UserCreate, User
from api.schemas.token import Token


router = APIRouter(prefix="/oauth2", tags=["public: oauth2"])


@router.post("/register", response_model=User)
async def register(user: UserCreate):
    return await our_register(user)


@router.post("/login", response_model=Token)
async def login_with_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await our_login(form_data)


@router.post("/verify_email")
async def verify_email(email: str):
    return await send_email_verification(email)


@router.post("/verify_email/callback")
async def authenticate_email(otp: str):
    return await email_authentication(otp)


@router.get("/login")
async def login(provider: str):
    if provider == "google":
        return await google_login()
    else:
        raise UnknownProvider


@router.get("/{provider}/callback", response_model=Token)
async def auth_callback(provider: str, request: Request):
    if provider == "google":
        return await google_auth_callback(request)
    else:
        raise UnknownProvider
