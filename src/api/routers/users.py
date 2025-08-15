"""/users router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import User, UserCreate
from database.supabase_connection import supabase_connection
from api.authentication.allowed_roles import admin_only, logged_only
from api.authentication.token import validate_token
from api.handlers.exceptions import DemandOwnerAccess
from config import settings


router = APIRouter(prefix="/users", tags=["users"])


"""/users endpoint"""
@router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    users = supabase_connection.fetch_all(settings.USER_TABLE)
    return users




"""/users/{user_id} endpoint"""
@router.get("/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user(user_id: int):
    user = supabase_connection.find_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user[0]

@router.put("/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserCreate):
    user = supabase_connection.update_by(
        settings.USER_TABLE,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    user = supabase_connection.delete_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user




"""/users/owner/{user_id} endpoint"""
@router.put("/owner/{user_id}", response_model=User, dependencies=[Depends(logged_only)])
async def update_owner(user_id: int, user: UserCreate, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    user = supabase_connection.update_by(
        settings.USER_TABLE,
        "id",
        user_id, 
        user.model_dump(),
    )
    return user

@router.delete("/owner/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    user = supabase_connection.delete_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user




"""/users/name/{username} endpoint"""
@router.get("/name/{username}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_name(username: str):
    user = supabase_connection.find_ilike(
        settings.USER_TABLE,
        "username",
        username,
    )
    return user[0]




"""/users/email/{email} endpoint"""
@router.get("/email/{email}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_email(email: str):
    user = supabase_connection.find_ilike(
        settings.USER_TABLE,
        "email",
        email,
    )
    return user[0]