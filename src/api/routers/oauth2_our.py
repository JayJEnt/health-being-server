"""/oauth2_our endpoint"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from typing import Annotated

from api.schemas.user import UserCreate, User
from api.schemas.token import Token
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.routers.users_email_email import get_user_by_email
from api.handlers.exceptions import RescourceAlreadyTaken, RescourceNotFound, InvalidCredentials
from authentication.hash_methods import hash_password
from authentication.authentication import authenticate_user, create_access_token
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/oauth2_our", tags=["oauth2_our"])


@router.post("/register", response_model=User)
async def create_user(user: UserCreate, other_provider: bool=False):
    try:
        user_response = await get_user_by_email(user.email)
        logger.error(f"Email: {user.email} is already registered in our base.")
        raise RescourceAlreadyTaken
    
    except RescourceNotFound:
        if not other_provider:
            user, password = pop_attributes(user, ["password"])
            hashed_password = hash_password(password[0])
            user = add_attributes(user, [{"hashed_password": hashed_password},{"role": "user"}])
        else:
            user = add_attributes(user, [{"role": "user"}])
        
        user = supabase_connection.insert(
            settings.user_table,
            user,
        )
        logger.info(f"Email: {user.email} is successfully registered.")
        return user
    
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