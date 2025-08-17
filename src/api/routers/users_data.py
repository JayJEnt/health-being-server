"""/users_data router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import UserData, UserDataCreate, User
from api.authentication.allowed_roles import admin_only, logged_only
from api.crud.get_methods import get_elements, get_element_by_id
from api.crud.delete_methods import delete_element_by_id
from api.crud.put_methods import update_element_by_id
from api.authentication.token import validate_token
from api.handlers.exceptions import DemandOwnerAccess


router = APIRouter(prefix="/users_data", tags=["users_data"])


"""/users_data endpoint"""
@router.get("", response_model=List[UserData], dependencies=[Depends(admin_only)])
async def get_users_data():
    return await get_elements("user_data")




"""/users_data/{user_id} endpoint"""
@router.get("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def get_user_data(user_id: int):
    return await get_element_by_id("user_data", user_id)

@router.put("/{user_id}", response_model=UserData, dependencies=[Depends(admin_only)])
async def update_user_data(user_id: int, user: UserDataCreate):
    return await update_element_by_id("user_data", user_id, user)

@router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user_data(user_id: int):
    return await delete_element_by_id("user_data", user_id)




"""/users_data/owner/{user_id} endpoint"""
@router.get("/owner/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def get_owner_data(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    return await get_element_by_id("user_data", user_id)

@router.put("/owner/{user_id}", response_model=UserData, dependencies=[Depends(logged_only)])
async def update_owner_data(user_id: int, user: UserDataCreate, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    return await update_element_by_id("user_data", user_id, user)

@router.delete("/owner/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner_data(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user["id"]:
        raise DemandOwnerAccess
    return await delete_element_by_id("user_data", user_id)