"""/diet_types/name/{diet_name} endpoint"""
from fastapi import APIRouter

from api.schemas.diet_type import DietType
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/diet_types/name/{diet_name}", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    diet_type = supabase_connection.find_by(
        settings.diet_type_table,
        "diet_name",
        diet_name,
    )
    return diet_type