"""/users_data router"""
from fastapi import APIRouter, Depends

from api.schemas.user import UserData, UserDataCreate, User
from api.authentication.allowed_roles import admin_only, logged_only, owner_only
from api.crud.single_entity.get_methods import get_element_by_id
from api.crud.single_entity.delete_methods import delete_element_by_id
from api.crud.single_entity.put_methods import update_element_by_id
from api.authentication.token import validate_token


router = APIRouter(prefix="/users_data", tags=["users_data"])


"""/users_data/{user_id} endpoint"""
@router.get("/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def get_owner_data(user_id: int, requesting_user: User = Depends(validate_token)):
    owner_only("user_data", user_id, requesting_user)

    return await get_element_by_id("user_data", user_id)


@router.put("/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def update_owner_data(user_id: int, user: UserDataCreate, requesting_user: User = Depends(validate_token)):
    owner_only("user_data", user_id, requesting_user)

    return await update_element_by_id("user_data", user_id, user)


@router.delete("/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner_data(user_id: int, requesting_user: User = Depends(validate_token)):
    owner_only("user_data", user_id, requesting_user)

    return await delete_element_by_id("user_data", user_id)




admin_router = APIRouter(prefix="/admin/users_data", tags=["admin: users_data"])


"""/admin/users_data/{user_id} endpoint"""
@admin_router.get("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def get_user_data(user_id: int):
    return await get_element_by_id("user_data", user_id)


@admin_router.put("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def update_user_data(user_id: int, user: UserDataCreate):
    return await update_element_by_id("user_data", user_id, user)


@admin_router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user_data(user_id: int):
    return await delete_element_by_id("user_data", user_id)