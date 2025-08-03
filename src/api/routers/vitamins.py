"""/vitamins endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.vitamin import VitaminCreate, Vitamin
from database.supabase_connection import supabase_connection
from authentication.allowed_roles import admin_only
from config import settings


router = APIRouter()


@router.get("/vitamins", response_model=List[Vitamin])
async def get_vitamins():
    vitamins = supabase_connection.fetch_all(settings.vitamin_table)
    return vitamins

@router.post("/vitamins", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    vitamin = supabase_connection.insert(
        settings.vitamin_table,
        vitamin.model_dump(),
    )
    return vitamin