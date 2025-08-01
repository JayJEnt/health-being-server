from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Optional, Annotated

from src.authentication.hash_methods import verify_password
from src.api.schemas.user import User
from src.api.routers.users_name_user_name import get_user_by_name
from src.api.handlers.exceptions import InvalidToken, RescourceNotFound
from src.config import settings
from src.logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    try:
        user_dict = await get_user_by_name(username)
    except RescourceNotFound:
        user_dict = None
    if not user_dict:
        return False
    user = User(**user_dict)
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.info("Validate token")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise InvalidToken
    except JWTError:
        raise InvalidToken
    
    user = await get_user_by_name(username)
    if user is None:
        raise InvalidToken
    
    return user