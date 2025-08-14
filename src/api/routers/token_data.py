"""/token_data endpoint"""
from fastapi import APIRouter, Depends

from typing import Annotated

from api.schemas.user import User
from authentication.authentication import validate_token


router = APIRouter(prefix="/token_data/owner", tags=["token_data"])


@router.get("", response_model=User)
async def get_token_owner(user: Annotated[User, Depends(validate_token)]):
    return user

@router.get("/admin_role", response_model=bool)
async def is_user_an_admin(user: Annotated[User, Depends(validate_token)]):
    return user["role"] == "admin"