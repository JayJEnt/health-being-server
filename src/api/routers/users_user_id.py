"""/users/{user_id} endpoint"""
from fastapi import APIRouter

from src.api.schemas.user import UserCreate, User
from src.database.supabase_connection import supabase_connection
from src.authentication.admin_access import only_admin_allowed
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

@router.put("/users/{user_id}", response_model=User)
@only_admin_allowed
async def update_user(user_id: int, user: UserCreate):
    user = supabase_connection.update_by(
        settings.user_table,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("/users/{user_id}")
@only_admin_allowed
async def delete_user(user_id: int):
    user = supabase_connection.delete_by(
        settings.user_table,
        "id",
        user_id,
    )
    return user

# TODO: add other endpoint to modify/delete, for each logged user, for his own data or modify access @staticmethod