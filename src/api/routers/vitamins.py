"""/vitamins endpoint"""
from fastapi import APIRouter

from typing import List

from src.api.schemas.vitamin import VitaminCreate, Vitamin
from src.database.supabase_connection import supabase_connection
from src.authentication.admin_access import only_admin_allowed
from src.config import settings


router = APIRouter()


@router.get("/vitamins", response_model=List[Vitamin])
async def get_vitamins():
    vitamins = supabase_connection.fetch_all(settings.vitamin_table)
    return vitamins

@router.post("/vitamins", response_model=Vitamin)
@only_admin_allowed
async def create_vitamin(vitamin: VitaminCreate):
    vitamin = supabase_connection.insert(
        settings.vitamin_table,
        vitamin.model_dump(),
    )
    return vitamin