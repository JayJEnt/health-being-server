"""/users_data router"""
from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only, logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.user import UserData, UserDataCreate, User


router = APIRouter(prefix="/users_data", tags=["users_data"])
crud = CrudOperations("user_data")


"""/users_data/{user_id} endpoint"""
@router.get("/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def get_owner_data(requesting_user: User = Depends(validate_token)):
    return await crud.get_by_id(requesting_user.id)


@router.put("/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def update_owner_data(user: UserDataCreate, requesting_user: User = Depends(validate_token)):
    return await crud.put(requesting_user.id, user)


@router.delete("/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner_data(requesting_user: User = Depends(validate_token)):
    return await crud.delete(requesting_user.id)




admin_router = APIRouter(prefix="/admin/users_data", tags=["admin: users_data"])


"""/admin/users_data/{user_id} endpoint"""
@admin_router.get("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def get_user_data(user_id: int):
    return await crud.get_by_id(user_id)


@admin_router.put("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def update_user_data(user_id: int, user: UserDataCreate):
    return await crud.put(user_id, user)


@admin_router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user_data(user_id: int):
    return await crud.delete(user_id)