"""/diet_types endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.diet_type import DietTypeCreate, DietType
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/diet_types", tags=["diet_types"])


@router.get("", response_model=List[DietType])
async def get_diet_types():
    diet_types = supabase_connection.fetch_all(settings.DIET_TYPE_TABLE)
    return diet_types

@router.post("", response_model=DietType, dependencies=[Depends(admin_only)])
async def create_diet_type(diet_type: DietTypeCreate):
    diet_type = supabase_connection.insert(
        settings.DIET_TYPE_TABLE,
        diet_type.model_dump(),
    )
    return diet_type