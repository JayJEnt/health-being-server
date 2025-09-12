"""/oauth2 router"""

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from api.authentication.oauth2_google import google_login, google_auth_callback
from api.authentication.oauth2_our import our_login, register
from api.handlers.exceptions import UnknownProvider
from api.schemas.user import UserCreate, User
from api.schemas.token import Token


router = APIRouter(prefix="/oauth2", tags=["oauth2"])


"""/oauth2_{external_provider}/login endpoint"""


@router.get("_{external_provider}/login")  # TODO CHANGE URL AFTER UPDATE
async def login(external_provider: str):
    if external_provider == "google":
        return await google_login()
    else:
        raise UnknownProvider


"""/oauth2_{external_provider}/callback endpoint"""


@router.get("_google/callback", response_model=Token)  # TODO CHANGE URL AFTER UPDATE
async def auth_callback(request: Request):
    return await google_auth_callback(request)


"""/oauth2_our/login endpoint"""


@router.post("_our/login", response_model=Token)  # TODO CHANGE URL AFTER UPDATE
async def login_with_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await our_login(form_data)


"""/oauth2_our/register endpoint"""


@router.post("_our/register", response_model=User)
async def our_register(user: UserCreate):
    return await register(user)
