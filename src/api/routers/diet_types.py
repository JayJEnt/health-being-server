"""/diet_types endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.diet_type import DietTypeCreate, DietType
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/diet_types/", response_model=List[DietType])
async def get_diet_types():
    diet_types = supabase_connection.fetch_all(settings.diet_type_table)
    return diet_types

@router.post("/diet_types/", response_model=DietType)
async def create_diet_type(diet_type: DietTypeCreate):
    diet_type = supabase_connection.insert(
        settings.diet_type_table,
        diet_type.model_dump(),
    )
    return diet_type