"""/token_data router"""
from fastapi import APIRouter, Depends

from typing import Annotated

from api.schemas.user import User
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/token_data", tags=["token_data"])


"""/token_data/user endpoint"""
@router.get("/user", response_model=User, dependencies=[Depends(logged_only)])
async def get_token_owner(user: Annotated[User, Depends(validate_token)]):
    return user




"""/token_data/admin_role endpoint"""
@router.get("/admin_role", response_model=bool, dependencies=[Depends(logged_only)])
async def is_user_an_admin(user: Annotated[User, Depends(validate_token)]):
    return user.role == "admin"