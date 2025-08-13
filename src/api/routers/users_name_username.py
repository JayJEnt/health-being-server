"""/users/name/{username} endpoint"""
from fastapi import APIRouter

from api.schemas.user import User
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter(prefix="/users/name/{username}", tags=["users"])


@router.get("", response_model=User)
async def get_user_by_name(username: str):
    user = supabase_connection.find_by(
        settings.USER_TABLE,
        "username",
        username,
    )
    return user[0]