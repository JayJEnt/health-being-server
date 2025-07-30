"""/users endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.user import UserCreate, User
from authentication.hash_methods import hash_password
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/users/", response_model=List[User])
async def get_users():
    users = supabase_connection.fetch_all(settings.user_table)
    return users

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user, password = pop_attributes(user, ["password"])
    hashed_password = hash_password(password[0])
    user = add_attributes(user, [{"hashed_password": hashed_password},{"role": "user"}])
    user = supabase_connection.insert(
        settings.user_table,
        user,
    )
    return user