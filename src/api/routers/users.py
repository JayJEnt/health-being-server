"""/users router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import User, UserCreate, UserPostCreate
from api.authentication.allowed_roles import admin_only, logged_only
from api.crud.get_methods import get_elements, get_element_by_id, get_element_by_name
from api.crud.delete_methods import delete_element_by_id
from api.crud.put_methods import update_element_by_id
from api.authentication.token import validate_token
from api.handlers.exceptions import DemandOwnerAccess


router = APIRouter(prefix="/users", tags=["users"])


"""/users endpoint"""
@router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    return await get_elements("user")




"""/users/{user_id} endpoint"""
@router.get("/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user(user_id: int):
    return await get_element_by_id("user", user_id)

@router.put("/{user_id}", response_model=UserPostCreate, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserCreate):
    return await update_element_by_id("user", user_id, user)

@router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    return await delete_element_by_id("user", user_id)




"""/users/owner/{user_id} endpoint"""
@router.get("/owner/{user_id}", response_model=User, dependencies=[Depends(logged_only)]) # seperated
async def get_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user.id:
        raise DemandOwnerAccess
    return await get_element_by_id("user", user_id)

@router.put("/owner/{user_id}", response_model=UserPostCreate, dependencies=[Depends(logged_only)])
async def update_owner(user_id: int, user: UserCreate, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user.id:
        raise DemandOwnerAccess
    return await update_element_by_id("user", user_id, user)

@router.delete("/owner/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    if user_id != requesting_user.id:
        raise DemandOwnerAccess
    return await delete_element_by_id("user", user_id)




"""/users/name/{username} endpoint"""
@router.get("/name/{username}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_name(username: str):
    return await get_element_by_name("user", username)




"""/users/email/{email} endpoint"""
@router.get("/email/{email}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_email(email: str):
    return await get_element_by_name("user", email, alternative_name=True)