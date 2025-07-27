"""/users/{user_id} endpoint"""
from fastapi import APIRouter

from api.schemas.user import UserCreate, User
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = supabase_connection.find_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    user = supabase_connection.update_by(
        settings.user_table,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = supabase_connection.delete_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user