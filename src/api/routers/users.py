"""/users router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.user import User, UserUpdate, UserUpdateAdmin, UserPostCreate
from api.authentication.allowed_roles import admin_only, logged_only
from api.crud.crud_operations import CrudOperations
from api.authentication.token import validate_token
from api.authentication.oauth2_our import hash_pass_for_user, hash_pass_for_admin


router = APIRouter(prefix="/users", tags=["users"])
crud = CrudOperations("user")


"""/users/{user_id} endpoint"""
@router.get("/{user_id}", response_model=UserPostCreate, dependencies=[Depends(logged_only)])
async def get_owner(requesting_user: User = Depends(validate_token)):
    return await crud.get_all(requesting_user.id, nested_attributes=["user_data"])


@router.put("/{user_id}", response_model=User, dependencies=[Depends(logged_only)])
async def update_owner(user: UserUpdate, requesting_user: User = Depends(validate_token)):
    user = await hash_pass_for_user(user)
    return await crud.put_all(requesting_user.id, user)


@router.delete("/{user_id}", dependencies=[Depends(logged_only)])
async def delete_owner(requesting_user: User = Depends(validate_token)):
    return await crud.delete_all(
        requesting_user.id,
        related_attributes=[
            "follows",
            "prefered_ingredients",
            "prefered_recipe_type",
            "recipe_favourite",
            "refrigerator"
        ],
        nested_attributes=["user_data"]
    )




admin_router = APIRouter(prefix="/admin/users", tags=["admin: users"])


"""/admin/users endpoint"""
@admin_router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    return await crud.get()




"""/admin/users/{user_id} endpoint"""
@admin_router.get("/{user_id}", response_model=UserPostCreate, dependencies=[Depends(admin_only)])
async def get_user(user_id: int):
    return await crud.get_all(user_id, nested_attributes=["user_data"])


@admin_router.put("/{user_id}", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user_id: int, user: UserUpdateAdmin):
    user = await hash_pass_for_admin(user)
    return await crud.put_all(user_id, user)


@admin_router.delete("/{user_id}", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    return await crud.delete_all(user_id)




"""/admin/users/name/{username} endpoint"""
@admin_router.get("/name/{username}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_name(username: str):
    return await crud.get_by_name(username)




"""/admin/users/email/{email} endpoint"""
@admin_router.get("/email/{email}", response_model=User, dependencies=[Depends(admin_only)])
async def get_user_by_email(email: str):
    return await crud.get_by_name(email, alternative_name=True)