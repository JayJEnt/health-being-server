"""/login endpoint"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from typing import Annotated

from api.schemas.token import Token
from authentication.authentication import authenticate_user, create_access_token
from api.handlers.exceptions import InvalidCredentials
from config import settings
from logger import logger


router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentials
    access_token_expires = timedelta(minutes=settings.access_token_expire)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
