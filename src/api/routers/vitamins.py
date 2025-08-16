"""/vitamins router"""
from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operator import (
    get_elements,
    create_element,
    delete_element_by_id,
    get_element_by_id,
    get_element_by_name,
    update_element_by_id,
)
from api.schemas.vitamin import VitaminCreate, Vitamin


router = APIRouter(prefix="/vitamins", tags=["vitamins"])


"""/vitamins endpoint"""
@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    return await get_elements("vitamins")

@router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    return await create_element("vitamins", vitamin)




"""/vitamins/{vitamin_id} endpoint"""
@router.get("/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    return await get_element_by_id("vitamins", vitamin_id)

@router.put("/{vitamin_id}", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    return await update_element_by_id("vitamins", vitamin_id, vitamin)

@router.delete("/{vitamin_id}", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    return await delete_element_by_id("vitamins", vitamin_id)




"""/vitamins/name/{vitamin_name} endpoint"""
@router.get("/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    return await get_element_by_name("vitamins", vitamin_name)