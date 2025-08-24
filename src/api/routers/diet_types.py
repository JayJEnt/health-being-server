"""/diet_types router"""
from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.schemas.diet_type import DietTypeCreate, DietType


router = APIRouter(prefix="/diet_types", tags=["diet_types"])
crud = CrudOperations("diet_type")


"""/diet_types endpoint"""
@router.get("", response_model=List[DietType])
async def get_diet_types():
    return await crud.get()




"""/diet_types/{diet_type_id} endpoint"""
@router.get("/{diet_type_id}", response_model=DietType)
async def get_diet_type(diet_type_id: int):
    return await crud.get_by_id(diet_type_id)




"""/diet_types/name/{diet_name} endpoint"""
@router.get("/name/{diet_name}", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    return await crud.get_by_name(diet_name)




admin_router = APIRouter(prefix="/admin/diet_types", tags=["admin: diet_types"])


"""/admin/diet_types endpoint"""
@admin_router.post("", response_model=DietType, dependencies=[Depends(admin_only)])
async def create_diet_type(diet_type: DietTypeCreate):
    return await crud.post(diet_type)




"""/admin/diet_types/{diet_type_id} endpoint"""
@admin_router.put("/{diet_type_id}", response_model=DietType, dependencies=[Depends(admin_only)])
async def update_diet_type(diet_type_id: int, diet_type: DietTypeCreate):
    return await crud.put(diet_type_id, diet_type)


@admin_router.delete("/{diet_type_id}", dependencies=[Depends(admin_only)])
async def delete_diet_type(diet_type_id: int):
    return await crud.delete(diet_type_id)