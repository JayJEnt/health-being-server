"""/users_data router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.user_data import UserData, UserDataCreate


router = APIRouter(prefix="/users_data", tags=["admin: users_data"])
crud = CrudOperations("user_data")


@router.get("/", response_model=UserData, dependencies=[Depends(admin_only)])
async def get_user_data(user_id: int = None):
    if not user_id:
        raise DemandQueryParameter
    return await crud.get_by_id(user_id)


@router.put("/", response_model=UserData, dependencies=[Depends(admin_only)])
async def update_user_data(user: UserDataCreate, user_id: int = None):
    if not user_id:
        raise DemandQueryParameter
    return await crud.put(user_id, user)


@router.delete("/", response_model=UserData, dependencies=[Depends(admin_only)])
async def delete_user_data(user_id: int = None):
    if not user_id:
        raise DemandQueryParameter
    return await crud.delete(user_id)
