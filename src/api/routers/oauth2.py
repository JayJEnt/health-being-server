"""/oauth2 router"""
from fastapi import APIRouter, Request, Depends, HTTPException  # TODO: create custom exceptions
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from api.authentication.oauth2_google import google_login, google_auth_callback
from api.authentication.oauth2_our import our_login
from api.schemas.token import Token
from config import settings


router = APIRouter(prefix="/oauth2/{provider}", tags=["oauth2"])


"""/oauth2/{external_provider}/login endpoint"""
@router.get("/login")
async def login(provider: str):
    if provider == "google":
        return await google_login()
    elif provider == "our":
        raise HTTPException(status_code=405, detail="Use POST method for our provider")
    else:
        raise HTTPException(status_code=404, detail="Unknown provider")




"""/oauth2/{external_provider}/callback endpoint"""
@router.get("/callback", response_model=Token)
async def auth_callback(provider: str, request: Request):
    if provider == "google":
        return await google_auth_callback(request)
    else:
        raise HTTPException(status_code=404, detail="Unknown provider")




"""/oauth2/our/login endpoint"""
@router.post("/login", response_model=Token)
async def login_with_form(
    provider: str,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if provider == "our":
        return await our_login(form_data)
    elif provider in settings.EXTERNAL_PROVIDERS:
        raise HTTPException(status_code=405, detail="Use GET method for external providers")
    else:
        raise HTTPException(status_code=404, detail="Unknown provider")

