"""/token_data router"""
from fastapi import APIRouter, Depends

from typing import Annotated

from api.schemas.user import User
from api.authentication.token import validate_token


router = APIRouter(prefix="/token_data", tags=["token_data"])


"""/token_data/user endpoint"""
@router.get("/user", response_model=User)
async def get_token_owner(user: Annotated[User, Depends(validate_token)]):
    return user




"""/token_data/admin_role endpoint"""
@router.get("/admin_role", response_model=bool)
async def is_user_an_admin(user: Annotated[User, Depends(validate_token)]):
    return user["role"] == "admin"