"""/vitamins router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.vitamin import VitaminCreate, Vitamin


router = APIRouter(prefix="/vitamins", tags=["admin: vitamins"])
crud = CrudOperations("vitamins")


@router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    return await crud.post(vitamin)


@router.put("/", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin: VitaminCreate, vitamin_id: int = None):
    if not vitamin_id:
        raise DemandQueryParameter
    return await crud.put(vitamin_id, vitamin)


@router.delete("/", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int = None):
    if not vitamin_id:
        raise DemandQueryParameter
    return await crud.delete(vitamin_id)
