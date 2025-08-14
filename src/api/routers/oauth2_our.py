"""/oauth2_our endpoint"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from typing import Annotated

from api.schemas.user import UserCreate, User
from api.schemas.token import Token
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.utils.crud_operations import get_element_by_name
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
        user_response = get_element_by_name("user", user.email)
        logger.error(f"Email: {user.email} is already registered in our base.")
        raise RescourceAlreadyTaken
    
    except RescourceNotFound:
        if not other_provider:
            user, password = pop_attributes(user, ["password"])
            hashed_password = hash_password(password[0])
            user = add_attributes(user, [{"hashed_password": hashed_password},{"role": "user"}])
        else:
            user = add_attributes(user, [{"role": "user"}])
        
        user_response = supabase_connection.insert(
            settings.USER_TABLE,
            user,
        )
        logger.info(f"Email: {user['email']} is successfully registered.")
        return user_response
    
@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentials

    user_data = {
        "id": user.id,
        "username": user.username,
        "sub": user.email,
        "provider": "health-being-server"
    }

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

    access_token = create_access_token(
        data=user_data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}