"""/users/name/{username} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.user import User
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/users/name/{username}", tags=["users"])


@router.get("", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_name(username: str):
    user = supabase_connection.find_by(
        settings.USER_TABLE,
        "username",
        username,
    )
    return user[0]