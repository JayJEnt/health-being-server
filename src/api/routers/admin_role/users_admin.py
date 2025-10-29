"""/users router"""

from fastapi import APIRouter, Depends

from typing import List, Union

from api.authentication.allowed_roles import admin_only
from api.authentication.oauth2_our import hash_pass_for_user
from api.crud.crud_operations import CrudOperations
from api.schemas.user import User, UserUpdateAdmin


router = APIRouter(prefix="/users", tags=["admin: users"])
crud = CrudOperations("user")


@router.get(
    "", response_model=Union[User, List[User]], dependencies=[Depends(admin_only)]
)
async def get_users(user_id: int = None, username: str = None, email: str = None):
    if user_id:
        return await crud.get_by_id(user_id)
    if username:
        return await crud.get_by_name(username)
    if email:
        return await crud.get_by_name(email, "email")
    return await crud.get()


@router.put("", response_model=User, dependencies=[Depends(admin_only)])
async def update_user(user: UserUpdateAdmin, user_id: int):
    user = await hash_pass_for_user(user)
    return await crud.put(user_id, user)


@router.delete("", dependencies=[Depends(admin_only)])
async def delete_user(user_id: int):
    return await crud.delete_all(user_id)
