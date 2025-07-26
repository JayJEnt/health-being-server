"""/ingredients endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.ingredient import CreateDetailedIngredient, Ingredient
from api.routers.vitamins_name_vitamin_name import get_vitamin_by_name
from api.utils.operation_on_attributes import pop_attributes
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/ingredients/", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.ingredient_table)
    return ingredients

@router.post("/ingredients/", response_model=Ingredient)
async def create_ingredient(ingredient: CreateDetailedIngredient):
    ingredient, poped_attributes = pop_attributes(ingredient, ["vitamins"])

    ingredient = supabase_connection.insert(
        settings.ingredient_table,
        ingredient,
    )
    logger.debug(f"ingredient_response: {ingredient}")

    ingredient_id = ingredient[0]["id"]
    logger.debug(f"ingredient_id: {ingredient_id}")

    vitamins = poped_attributes[0]
    if vitamins:
        for vitamin in vitamins:
            exists = await get_vitamin_by_name(vitamin["name"])
            if exists:
                logger.debug(f"exists: {exists}")

                supabase_connection.insert(
                    settings.vitamins_included_table,
                    {
                        "ingredient_id": ingredient_id,
                        "vitamin_id": exists["id"]
                    },
                )

    return ingredient[0]
