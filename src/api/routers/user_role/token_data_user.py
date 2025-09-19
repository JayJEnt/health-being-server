"""/token_data router"""

from fastapi import APIRouter, Depends

from typing import Annotated, Any

from api.schemas.user import User
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token, refresh_token


router = APIRouter(prefix="/token_data", tags=["user: token_data"])


@router.get("/user", response_model=User, dependencies=[Depends(logged_only)])
async def get_token_owner(user: Annotated[User, Depends(validate_token)]):
    return user


@router.get("/admin_role", response_model=bool, dependencies=[Depends(logged_only)])
async def is_user_an_admin(user: Annotated[User, Depends(validate_token)]):
    return user.role == "admin"


@router.get("/refresh", response_model=Any, dependencies=[Depends(logged_only)])
async def refresh_token(token: Annotated[Any, Depends(refresh_token)]):
    if token:
        return token
