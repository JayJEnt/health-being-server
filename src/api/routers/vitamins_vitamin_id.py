"""/vitamins/{vitamin_id} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.vitamin import VitaminCreate, Vitamin
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/vitamins/{vitamin_id}", tags=["vitamins"])


@router.get("", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    vitamin = supabase_connection.find_by(
        settings.vitamin_table,
        "id",
        vitamin_id,
    )
    return vitamin[0]

@router.put("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    vitamin = supabase_connection.update_by(
        settings.vitamin_table,
        "id",
        vitamin_id, 
        vitamin.model_dump(),
    )
    return vitamin

@router.delete("", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    vitamin = supabase_connection.delete_by(
        settings.vitamin_table,
        "id",
        vitamin_id,
    )
    return vitamin