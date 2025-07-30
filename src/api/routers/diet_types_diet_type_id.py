"""/diet_types/{diet_type_id} endpoint"""
from fastapi import APIRouter

from src.api.schemas.diet_type import DietTypeCreate, DietType
from src.database.supabase_connection import supabase_connection
from src.authentication.admin_access import only_admin_allowed
from src.config import settings


router = APIRouter()


@router.get("/diet_types/{diet_type_id}", response_model=DietType)
async def get_diet_type(diet_type_id: int):
    diet_type = supabase_connection.find_by(
        settings.diet_type_table,
        "id",
        diet_type_id,
    )
    return diet_type[0]

@router.put("/diet_types/{diet_type_id}", response_model=DietType)
@only_admin_allowed
async def update_diet_type(diet_type_id: int, diet_type: DietTypeCreate):
    diet_type = supabase_connection.update_by(
        settings.diet_type_table,
        "id",
        diet_type_id, 
        diet_type.model_dump(),
    )
    return diet_type

@router.delete("/diet_types/{diet_type_id}")
@only_admin_allowed
async def delete_diet_type(diet_type_id: int):
    diet_type = supabase_connection.delete_by(
        settings.diet_type_table,
        "id",
        diet_type_id,
    )
    return diet_type