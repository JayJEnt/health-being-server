"""/users/owner/{user_id} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.user import UserCreate, User
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import logged_only
from authentication.authentication import validate_token
from api.handlers.exceptions import DemandOwnerAccess
from config import settings


router = APIRouter(prefix="/users/owner/{user_id}", tags=["users"])


@router.put("", response_model=User, dependencies=[Depends(logged_only)])
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

@router.delete("", dependencies=[Depends(logged_only)])
async def delete_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    user = supabase_connection.delete_by(
        settings.USER_TABLE,
        "id",
        user_id,
    )
    return user