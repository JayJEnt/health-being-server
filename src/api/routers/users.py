"""/users endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import User
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    users = supabase_connection.fetch_all(settings.USER_TABLE)
    return users
