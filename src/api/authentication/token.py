from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Optional, Annotated

from api.crud.get_methods import get_element_by_name
from api.handlers.exceptions import InvalidToken
from api.schemas.user import User
from config import settings
from logger import logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    logger.debug(f"Data: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.info("Validate token")
    try:
        logger.debug(f"Token: {token}")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.debug(f"Got payload: {payload}")
        email: str = payload.get("sub")
        if email is None:
            logger.debug(f"Email: {email}")
            raise InvalidToken
    except JWTError:
        raise InvalidToken
    
    user = await get_element_by_name("user", email, alternative_name=True)
    if user is None:
        raise InvalidToken
    user = User(**user)
    return user