"""/users/{user_id} endpoint"""
from fastapi import APIRouter, Depends

from src.api.schemas.user import UserCreate, User
from src.database.supabase_connection import supabase_connection
from src.authentication.allowed_roles import admin_only
from src.config import settings


router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = supabase_connection.find_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user[0]

@router.put("/users/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserCreate):
    user = supabase_connection.update_by(
        settings.user_table,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("/users/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    user = supabase_connection.delete_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user

# TODO: add other endpoint to modify/delete, for each logged user, for his own data or modify access @staticmethod