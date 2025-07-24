"""/users endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.user import CreateUser, User
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/users/", response_model=List[User])
async def get_users():
    users = supabase_connection.fetch_all(settings.user_table)
    return users

@router.post("/users/", response_model=List[User])
async def create_user(user: CreateUser):
    user = supabase_connection.insert(
        settings.user_table,
        user.model_dump(),
    )
    return user