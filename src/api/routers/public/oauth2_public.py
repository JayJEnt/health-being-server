"""/oauth2 router"""

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import asyncio
from typing import Annotated

from api.authentication.oauth2_google import google_login, google_auth_callback
from api.authentication.oauth2_our import our_login, our_register
from api.authentication.email_authentication import (
    send_verification_email,
    verify_email_token,
)
from api.crud.single_entity.put_methods import update_element_by_id
from api.handlers.http_exceptions import UnknownProvider
from api.schemas.enum_utils import Role
from api.schemas.user import UserCreate, User
from api.schemas.token import Token


router = APIRouter(prefix="/oauth2", tags=["public: oauth2"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=User)
async def register(user: UserCreate):
    message, response = await asyncio.gather(
        send_verification_email(user.email), our_register(user)
    )
    return response


@router.post("/login", response_model=Token)
async def login_with_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await our_login(form_data)


@router.post("/send_verification_email", response_model=dict)
async def send_email(email: str):
    return await send_verification_email(email)


@router.get("/verify_email", response_model=User)
async def verify_email(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await verify_email_token(token)
    return await update_element_by_id("user", user["id"], {"role": Role.user.value})


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
