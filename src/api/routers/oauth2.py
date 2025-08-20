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


"""/oauth2/{external_provider}/login endpoint"""
@router.get("/{provider}/login")
async def login(provider: str):
    if provider == "google":
        return await google_login()
    else:
        raise UnknownProvider




"""/oauth2/{external_provider}/callback endpoint"""
@router.get("/{provider}/callback", response_model=Token)
async def auth_callback(provider: str, request: Request):
    if provider == "google":
        return await google_auth_callback(request)
    else:
        raise UnknownProvider




"""/oauth2/our/login endpoint"""
@router.post("/our/login", response_model=Token)
async def login_with_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await our_login(form_data)
    




"""/oauth2/our/register endpoint"""
@router.post("/our/register", response_model=User)
async def our_register(user: UserCreate):
    return await register(user) 
