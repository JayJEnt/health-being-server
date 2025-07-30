"""/diet_types endpoint"""
from fastapi import APIRouter

from typing import List

from src.api.schemas.diet_type import DietTypeCreate, DietType
from src.database.supabase_connection import supabase_connection
from src.authentication.admin_access import only_admin_allowed
from src.config import settings


router = APIRouter()


@router.get("/diet_types", response_model=List[DietType])
async def get_diet_types():
    diet_types = supabase_connection.fetch_all(settings.diet_type_table)
    return diet_types

@router.post("/diet_types", response_model=DietType)
@only_admin_allowed
async def create_diet_type(diet_type: DietTypeCreate):
    diet_type = supabase_connection.insert(
        settings.diet_type_table,
        diet_type.model_dump(),
    )
    return diet_type