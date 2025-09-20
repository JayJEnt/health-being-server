"""/users router"""

from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.authentication.oauth2_our import hash_pass_for_admin
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.user import User, UserUpdateAdmin


router = APIRouter(prefix="/users", tags=["admin: users"])
crud = CrudOperations("user")


@router.get("", response_model=List[User], dependencies=[Depends(admin_only)])
async def get_users():
    return await crud.get()


# TODO: TEMP USER VALIDATION
@router.get("/", response_model=User, dependencies=[Depends(admin_only)])
async def get_user(user_id: int = None, username: str = None, email: str = None):
    if user_id:
        return await crud.get_all(user_id, nested_attributes=["user_data"])
    if username:
        return await crud.get_by_name(username)
    if email:
        return await crud.get_by_name(email, alternative_name=True)
    raise DemandQueryParameter


@router.put("/", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user: UserUpdateAdmin, user_id: int = None):
    if not user_id:
        raise DemandQueryParameter
    user = await hash_pass_for_admin(user)
    return await crud.put(user_id, user)


@router.delete("/", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int = None):
    if not user_id:
        raise DemandQueryParameter
    return await crud.delete_all(user_id, nested_attributes=["user_data"])
