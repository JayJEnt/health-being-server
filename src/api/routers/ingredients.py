"""/ingredients endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.ingredient import CreateIngredient, Ingredient
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/ingredients/", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.ingredient_table)
    return ingredients

@router.post("/ingredients/", response_model=Ingredient)
async def create_ingredient(ingredient: CreateIngredient):
    ingredient_json = ingredient.model_dump()

    vitamins = ingredient_json.get("vitamins", "")
    logger.debug(f"vitamins: {vitamins}")

    ingredient = {key : value for key, value in ingredient_json.items() if key != "vitamins"}
    logger.debug(f"ingredient: {ingredient}")

    ingredient = supabase_connection.insert(
        settings.ingredient_table,
        ingredient,
    )
    logger.debug(f"ingredient_response: {ingredient}")

    recipe_id = recipe[0]["id"]
    logger.debug(f"recipe_id: {recipe_id}")
    return ingredient[0]
