"""/vitamins endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.vitamin import CreateVitamin, Vitamin
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/vitamins/", response_model=List[Vitamin])
async def get_vitamins():
    vitamins = supabase_connection.fetch_all(settings.vitamin_table)
    return vitamins

@router.post("/vitamins/", response_model=Vitamin)
async def create_vitamin(vitamin: CreateVitamin):
    vitamin = supabase_connection.insert(
        settings.vitamin_table,
        vitamin.model_dump(),
    )
    return vitamin[0]