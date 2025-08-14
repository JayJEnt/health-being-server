"""/ingredients/name/{ingredient_name} endpoint"""
from fastapi import APIRouter

from api.schemas.ingredient import Ingredient
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter(prefix="/ingredients/name/{ingredient_name}", tags=["ingredients"])


@router.get("", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    ingredient = supabase_connection.find_ilike(
        settings.INGREDIENT_TABLE,
        "name",
        ingredient_name,
    )
    return ingredient[0]