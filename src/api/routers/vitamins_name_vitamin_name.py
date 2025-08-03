"""/vitamins/name/{vitamin_name} endpoint"""
from fastapi import APIRouter

from api.schemas.vitamin import Vitamin
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/vitamins/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    vitamin = supabase_connection.find_by(
        settings.vitamin_table,
        "name",
        vitamin_name,
    )
    return vitamin[0]