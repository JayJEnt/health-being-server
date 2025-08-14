"""/users/email/{email} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.user import User
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/users/email/{email}", tags=["users"])


@router.get("", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_email(email: str):
    user = supabase_connection.find_ilike(
        settings.USER_TABLE,
        "email",
        email,
    )
    return user[0]