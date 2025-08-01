"""/users/name/{user_name} endpoint"""
from fastapi import APIRouter

from src.api.schemas.user import User
from src.database.supabase_connection import supabase_connection
from src.config import settings


router = APIRouter()


@router.get("/users/name/{user_name}", response_model=User)
async def get_user_by_name(user_name: str):
    user = supabase_connection.find_by(
        settings.user_table,
        "username",
        user_name,
    )
    return user[0]