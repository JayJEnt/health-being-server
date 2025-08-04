"""/users/email/{email} endpoint"""
from fastapi import APIRouter

from api.schemas.user import User
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter(prefix="/users/email/{email}", tags=["users"])


@router.get("", response_model=User)
async def get_user_by_email(email: str):
    user = supabase_connection.find_by(
        settings.user_table,
        "email",
        email,
    )
    return user[0]