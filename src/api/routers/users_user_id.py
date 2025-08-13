"""/users/{user_id} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.user import UserCreate, User
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/users/{user_id}", tags=["users"])


@router.get("", response_model=User, dependencies=[Depends(admin_only)])
async def get_user(user_id: int):
    user = supabase_connection.find_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user[0]

@router.put("", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserCreate):
    user = supabase_connection.update_by(
        settings.USER_TABLE,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    user = supabase_connection.delete_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user
