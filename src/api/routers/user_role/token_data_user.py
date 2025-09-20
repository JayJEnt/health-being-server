"""/token_data router"""

from fastapi import APIRouter, Depends

from typing import Annotated, Dict, Union

from api.schemas.user import User
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token, refresh_token


router = APIRouter(prefix="/token_data", tags=["user: token_data"])


@router.get("", response_model=Union[User, bool], dependencies=[Depends(logged_only)])
async def get_token_data(
    user: Annotated[User, Depends(validate_token)],
    admin_role: bool = False,
):
    if admin_role:
        return user.role == "admin"
    return user


@router.get("/refresh", response_model=Dict, dependencies=[Depends(logged_only)])
async def refresh_token(token: Annotated[Dict, Depends(refresh_token)]):
    if token:
        return token
