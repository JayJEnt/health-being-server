"""/ingredients/name/{ingredient_name} endpoint"""
from fastapi import APIRouter

from api.schemas.ingredient import Ingredient
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/ingredients/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    ingredient = supabase_connection.find_by(
        settings.ingredient_table,
        "name",
        ingredient_name,
    )
    return ingredient