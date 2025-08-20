"""/users router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import User, UserUpdate, UserUpdateAdmin, UserPostCreate
from api.authentication.allowed_roles import admin_only, logged_only, owner_only
from api.crud.single_entity.get_methods import get_elements, get_element_by_name
from api.crud.entity_all_attached.get_methods import get_element_by_id
from api.crud.entity_all_attached.delete_methods import delete_element_by_id
from api.crud.entity_with_relations.put_methods import update_element_by_id
from api.authentication.token import validate_token
from api.authentication.oauth2_our import hash_pass_for_user, hash_pass_for_admin


router = APIRouter(prefix="/users", tags=["users"])


"""/users/{user_id} endpoint"""
@router.get("/{user_id}", response_model=UserPostCreate, dependencies=[Depends(logged_only)])
async def get_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    owner_only("user", user_id, requesting_user)
    
    return await get_element_by_id("user", user_id)


@router.put("/{user_id}", response_model=User, dependencies=[Depends(logged_only)])
async def update_owner(user_id: int, user: UserUpdate, requesting_user: User = Depends(validate_token)):
    owner_only("user", user_id, requesting_user)
    
    user = await hash_pass_for_user(user)
    return await update_element_by_id("user", user_id, user)


@router.delete("/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner(user_id: int, requesting_user: User = Depends(validate_token)):
    owner_only("user", user_id, requesting_user)
    
    return await delete_element_by_id("user", user_id)




admin_router = APIRouter(prefix="/admin/users", tags=["admin: users"])


"""/admin/users endpoint"""
@admin_router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    return await get_elements("user")




"""/admin/users/{user_id} endpoint"""
@admin_router.get("/{user_id}", response_model=UserPostCreate, dependencies=[Depends(admin_only)])
async def get_user(user_id: int):
    return await get_element_by_id("user", user_id)


@admin_router.put("/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserUpdateAdmin):
    user = await hash_pass_for_admin(user)
    return await update_element_by_id("user", user_id, user)


@admin_router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    return await delete_element_by_id("user", user_id)




"""/admin/users/name/{username} endpoint"""
@admin_router.get("/name/{username}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_name(username: str):
    return await get_element_by_name("user", username)




"""/admin/users/email/{email} endpoint"""
@admin_router.get("/email/{email}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_email(email: str):
    return await get_element_by_name("user", email, alternative_name=True)