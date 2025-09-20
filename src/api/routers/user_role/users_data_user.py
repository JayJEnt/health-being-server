"""/users_data router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.crud.utils import add_attributes
from api.schemas.user import User
from api.schemas.user_data import UserData, UserDataCreate


router = APIRouter(prefix="/users_data/owner", tags=["user: users_data"])
crud = CrudOperations("user_data")


@router.get("", response_model=UserData, dependencies=[Depends(logged_only)])
async def get_owner_data(requesting_user: User = Depends(validate_token)):
    return await crud.get_by_id(requesting_user.id)


@router.put("", response_model=UserData, dependencies=[Depends(logged_only)])
async def update_owner_data(
    user: UserDataCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.put(requesting_user.id, user)


@router.post("", response_model=UserData, dependencies=[Depends(logged_only)])
async def create_owner_data(
    user: UserDataCreate, requesting_user: User = Depends(validate_token)
):
    user = add_attributes(user, [{"user_id": requesting_user.id}])
    return await crud.post(user)


@router.delete("", response_model=UserData, dependencies=[Depends(logged_only)])
async def delete_owner_data(requesting_user: User = Depends(validate_token)):
    return await crud.delete(requesting_user.id)
