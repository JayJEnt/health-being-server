"""/diet_types/name/{diet_name} endpoint"""
from fastapi import APIRouter

from api.schemas.diet_type import DietType
from database.supabase_connection import supabase_connection
from api.utils.crud_operations import get_element_by_name
from config import settings


router = APIRouter(prefix="/diet_types/name/{diet_name}", tags=["diet_types"])


@router.get("", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    diet_type = get_element_by_name("diet_type", diet_name)
    return diet_type