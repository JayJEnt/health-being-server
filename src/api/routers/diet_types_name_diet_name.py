"""/diet_types/name/{diet_name} endpoint"""
from fastapi import APIRouter

from api.schemas.diet_type import DietType
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter(prefix="/diet_types/name/{diet_name}", tags=["diet_types"])


@router.get("", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    diet_type = supabase_connection.find_ilike(
        settings.DIET_TYPE_TABLE,
        "diet_name",
        diet_name,
    )
    return diet_type[0]