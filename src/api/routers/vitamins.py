"""/vitamins router"""
from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.crud.single_entity.get_methods import get_elements, get_element_by_id, get_element_by_name
from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.delete_methods import delete_element_by_id
from api.crud.entity_with_relations.put_methods import update_element_by_id
from api.schemas.vitamin import VitaminCreate, Vitamin


router = APIRouter(prefix="/vitamins", tags=["vitamins"])


"""/vitamins endpoint"""
@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    return await get_elements("vitamins")




"""/vitamins/{vitamin_id} endpoint"""
@router.get("/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    return await get_element_by_id("vitamins", vitamin_id)




"""/vitamins/name/{vitamin_name} endpoint"""
@router.get("/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    return await get_element_by_name("vitamins", vitamin_name)




admin_router = APIRouter(prefix="/admin/vitamins", tags=["admin: vitamins"])


"""/admin/vitamins endpoint"""
@admin_router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    return await create_element("vitamins", vitamin)




"""/admin/vitamins/{vitamin_id} endpoint"""
@admin_router.put("/{vitamin_id}", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    return await update_element_by_id("vitamins", vitamin_id, vitamin)


@admin_router.delete("/{vitamin_id}", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    return await delete_element_by_id("vitamins", vitamin_id)
