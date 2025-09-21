from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from typing import Annotated

from api.authentication.hash_methods import verify_password, hash_password
from api.authentication.token import create_access_token
from api.handlers.http_exceptions import (
    ResourceAlreadyTaken,
    ResourceNotFound,
    InvalidCredentials,
)
from api.schemas.user import UserOurAuth, UserCreate, UserUpdateAdmin
from api.crud.single_entity.get_methods import get_element_by_name
from api.crud.single_entity.post_methods import create_element
from api.crud.utils import pop_attributes, add_attributes
from config import settings
from logger import logger


async def authenticate_user(email: str, password: str):
    try:
        user_dict = await get_element_by_name("user", email, alternative_name=True)
    except ResourceNotFound:
        user_dict = None
    if not user_dict:
        return False
    user = UserOurAuth(**user_dict)
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def our_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentials

    user_data = {
        "id": user.id,
        "username": user.username,
        "sub": user.email,
        "provider": "health-being-server",
    }

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

    access_token = create_access_token(
        data=user_data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def register(user: UserCreate, other_provider: bool = False):
    try:
        user_response = await get_element_by_name(
            "user", user.email, alternative_name=True
        )
        raise ResourceAlreadyTaken

    except ResourceAlreadyTaken:
        logger.info(
            f"Email: {user.email} is already registered in our base."
            f" Try to log into."
        )

    except ResourceNotFound:
        if not other_provider:
            user = await hash_pass_for_user(user)
        else:
            user = add_attributes(user, [{"role": "user"}])

        user_response = await create_element("user", user)
        logger.info(
            f"Email: {user['email']} is successfully registered."
            f" Now you can log into."
        )

    return user_response


async def hash_pass_for_user(user: UserCreate):
    user, password = pop_attributes(user, ["password"])
    hashed_password = hash_password(password[0].get("password", ""))
    return add_attributes(
        user, [{"hashed_password": hashed_password}, {"role": "user"}]
    )


async def hash_pass_for_admin(user: UserUpdateAdmin):
    user, password = pop_attributes(user, ["password"])
    hashed_password = hash_password(password[0].get("password", ""))
    return add_attributes(user, [{"hashed_password": hashed_password}])
