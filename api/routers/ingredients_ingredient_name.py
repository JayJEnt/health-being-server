"""/ingredients/{ingredient_name} endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.ingredient import CreateIngredient, Ingredient
from db_conn import supabase_connection
from config import settings


router = APIRouter()


@router.get("/ingredients/{ingredient_name}", response_model=List[Ingredient])
async def get_ingredient_by_name(ingredient_name: str):
    ingredient = supabase_connection.find_by(
        settings.ingredient_table,
        "name",
        ingredient_name,
    )
    return ingredient