from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated, Any

from api.crud.single_entity.get_methods import get_element_by_name
from api.handlers.exceptions import InvalidToken, ResourceNotFound
from api.schemas.user import User
from config import settings
from logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    logger.info("Creating a new token...")

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    logger.info("Validating token...")

    payload = await get_payload_from_token(token)
    user = await get_user_from_token(payload)

    return user


async def get_payload_from_token(token: str) -> dict:
    try:
        logger.info("Got payload")
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise InvalidToken


async def get_user_from_token(payload: dict) -> dict:
    email: str = payload.get("sub", None)
    if email is None:
        raise InvalidToken

    try:
        user = await get_element_by_name("user", email, alternative_name=True)
        logger.info("Got User")
        return User(**user)
    except ResourceNotFound:
        raise InvalidToken


async def time_for_refresh(payload: dict, time_delta: timedelta) -> bool:
    exp_timestamp = payload.get("exp", None)
    if exp_timestamp is None:
        raise InvalidToken

    expire_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)

    remaining = expire_time - now

    return remaining < time_delta


async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Any:
    logger.info("Checking if token is supposed to refresh...")
    payload = await get_payload_from_token(token)

    if await time_for_refresh(payload, timedelta(minutes=5)):
        provider = payload.get("provider", None)
        user = await get_user_from_token(payload)
        user_data = {
            "id": user.id,
            "username": user.username,
            "sub": user.email,
            "provider": provider,
        }
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        access_token = create_access_token(
            data=user_data, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    return None
