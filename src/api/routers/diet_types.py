"""/diet_types router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.diet_type import DietTypeCreate, DietType
from api.authentication.allowed_roles import admin_only
from api.crud.single_entity.get_methods import get_elements, get_element_by_id, get_element_by_name
from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.delete_methods import delete_element_by_id
from api.crud.single_entity.put_methods import update_element_by_id


router = APIRouter(prefix="/diet_types", tags=["diet_types"])


"""/diet_types endpoint"""
@router.get("", response_model=List[DietType])
async def get_diet_types():
    return await get_elements("diet_type")




"""/diet_types/{diet_type_id} endpoint"""
@router.get("/{diet_type_id}", response_model=DietType)
async def get_diet_type(diet_type_id: int):
    return await get_element_by_id("diet_type", diet_type_id)




"""/diet_types/name/{diet_name} endpoint"""
@router.get("/name/{diet_name}", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    return await get_element_by_name("diet_type", diet_name)




admin_router = APIRouter(prefix="/admin/diet_types", tags=["admin: diet_types"])


"""/admin/diet_types endpoint"""
@admin_router.post("", response_model=DietType, dependencies=[Depends(admin_only)])
async def create_diet_type(diet_type: DietTypeCreate):
    return await create_element("diet_type", diet_type)




"""/admin/diet_types/{diet_type_id} endpoint"""
@admin_router.put("/{diet_type_id}", response_model=DietType, dependencies=[Depends(admin_only)])
async def update_diet_type(diet_type_id: int, diet_type: DietTypeCreate):
    return await update_element_by_id("diet_type", diet_type_id, diet_type)


@admin_router.delete("/{diet_type_id}", dependencies=[Depends(admin_only)])
async def delete_diet_type(diet_type_id: int):
    return await delete_element_by_id("diet_type", diet_type_id)