"""/users endpoint"""
from fastapi import APIRouter

from typing import List

from src.api.schemas.user import UserCreate, User
from src.authentication.hash_methods import hash_password
from src.api.utils.operations_on_attributes import pop_attributes, add_attributes
from src.database.supabase_connection import supabase_connection
from src.config import settings


router = APIRouter()


@router.get("/users", response_model=List[User])
async def get_users():
    users = supabase_connection.fetch_all(settings.user_table)
    return users
