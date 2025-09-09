"""/vitamins router"""

from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.schemas.vitamin import VitaminCreate, Vitamin


router = APIRouter(prefix="/vitamins", tags=["vitamins"])
crud = CrudOperations("vitamins")


"""/vitamins endpoint"""


@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    return await crud.get()


"""/vitamins/{vitamin_id} endpoint"""


@router.get("/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    return await crud.get_by_id(vitamin_id)


"""/vitamins/name/{vitamin_name} endpoint"""


@router.get("/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    return await crud.get_by_name(vitamin_name)


admin_router = APIRouter(prefix="/admin/vitamins", tags=["admin: vitamins"])


"""/admin/vitamins endpoint"""


@admin_router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    return await crud.post(vitamin)


"""/admin/vitamins/{vitamin_id} endpoint"""


@admin_router.put(
    "/{vitamin_id}", response_model=Vitamin, dependencies=[Depends(admin_only)]
)
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    return await crud.put(vitamin_id, vitamin)


@admin_router.delete("/{vitamin_id}", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    return await crud.delete(vitamin_id)
