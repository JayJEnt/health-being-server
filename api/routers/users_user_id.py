"""/users/{user_id} endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.user import CreateUser, User
from db_conn import supabase_connection
from config import settings


router = APIRouter()


@router.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int):
    user = supabase_connection.find_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user

@router.put("/users/{user_id}", response_model=List[User])
async def update_user(user_id: int, user: CreateUser):
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