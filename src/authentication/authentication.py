from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Optional, Annotated

from authentication.hash_methods import verify_password
from api.schemas.user import UserOurAuthentication
from api.routers.users_email_email import get_user_by_email
from api.handlers.exceptions import InvalidToken, RescourceNotFound
from config import settings
from logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(email: str, password: str):
    try:
        user_dict = await get_user_by_email(email)
    except RescourceNotFound:
        user_dict = None
    if not user_dict:
        return False
    user = UserOurAuthentication(**user_dict)
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
        email: str = payload.get("sub")
        if email is None:
            raise InvalidToken
    except JWTError:
        raise InvalidToken
    
    user = await get_user_by_email(email)
    if user is None:
        raise InvalidToken
    
    return user