"""/ingredients endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.ingredient import CreateIngredient, Ingredient
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/ingredients/", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.ingredient_table)
    return ingredients

@router.post("/ingredients/", response_model=List[Ingredient])
async def create_ingredient(ingredient: CreateIngredient):
    ingredient = supabase_connection.insert(
        settings.ingredient_table,
        ingredient.model_dump(),
    )
    return ingredient
