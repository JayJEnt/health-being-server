"""/diet_types router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.diet_type import DietTypeCreate, DietType
from database.supabase_connection import supabase_connection
from api.authentication.allowed_roles import admin_only
from config import settings


router = APIRouter(prefix="/diet_types", tags=["diet_types"])


"""/diet_types endpoint"""
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




"""/diet_types/{diet_type_id} endpoint"""
@router.get("/{diet_type_id}", response_model=DietType)
async def get_diet_type(diet_type_id: int):
    diet_type = supabase_connection.find_by(
        settings.DIET_TYPE_TABLE,
        "id",
        diet_type_id,
    )
    return diet_type[0]

@router.put("/{diet_type_id}", response_model=DietType, dependencies=[Depends(admin_only)])
async def update_diet_type(diet_type_id: int, diet_type: DietTypeCreate):
    diet_type = supabase_connection.update_by(
        settings.DIET_TYPE_TABLE,
        "id",
        diet_type_id, 
        diet_type.model_dump(),
    )
    return diet_type

@router.delete("/{diet_type_id}", dependencies=[Depends(admin_only)])
async def delete_diet_type(diet_type_id: int):
    diet_type = supabase_connection.delete_by(
        settings.DIET_TYPE_TABLE,
        "id",
        diet_type_id,
    )
    return diet_type




"""/diet_types/name/{diet_name} endpoint"""
@router.get("/name/{diet_name}", response_model=DietType)
async def get_diet_by_name(diet_name: str):
    diet_type = supabase_connection.find_ilike(
        settings.DIET_TYPE_TABLE,
        "diet_name",
        diet_name,
    )
    return diet_type[0]