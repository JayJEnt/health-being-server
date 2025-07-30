"""/vitamins/{vitamin_id} endpoint"""
from fastapi import APIRouter

from api.schemas.vitamin import VitaminCreate, Vitamin
from database.supabase_connection import supabase_connection
from authentication.admin_access import only_admin_allowed
from config import settings


router = APIRouter()


@router.get("/vitamins/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    vitamin = supabase_connection.find_by(
        settings.vitamin_table,
        "id",
        vitamin_id,
    )
    return vitamin[0]

@router.put("/vitamins/{vitamin_id}", response_model=Vitamin)
@only_admin_allowed
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    vitamin = supabase_connection.update_by(
        settings.vitamin_table,
        "id",
        vitamin_id, 
        vitamin.model_dump(),
    )
    return vitamin

@router.delete("/vitamins/{vitamin_id}")
@only_admin_allowed
async def delete_vitamin(vitamin_id: int):
    vitamin = supabase_connection.delete_by(
        settings.vitamin_table,
        "id",
        vitamin_id,
    )
    return vitamin