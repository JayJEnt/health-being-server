"""/vitamins router"""
from fastapi import APIRouter, Depends

from typing import List

from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from api.utils.crud_operations import create_element, delete_element, get_element_by_id, get_element_by_name
from api.schemas.vitamin import VitaminCreate, Vitamin
from config import settings


router = APIRouter(prefix="/vitamins", tags=["vitamins"])


"""/vitamins endpoint"""
@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    vitamins = supabase_connection.fetch_all(settings.VITAMIN_TABLE)
    return vitamins

@router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    return await create_element("vitamins", vitamin)




"""/vitamins/{vitamin_id} endpoint"""
@router.get("/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    return await get_element_by_id("vitamins", vitamin_id)

@router.put("/{vitamin_id}", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    vitamin = supabase_connection.update_by(
        settings.VITAMIN_TABLE,
        "id",
        vitamin_id, 
        vitamin.model_dump(),
    )
    return vitamin

@router.delete("/{vitamin_id}", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    return await delete_element("vitamins", vitamin_id)




"""/vitamins/name/{vitamin_name} endpoint"""
@router.get("/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    return await get_element_by_name("vitamins", vitamin_name)