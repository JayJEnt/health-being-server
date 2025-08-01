"""/ingredients endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from src.api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse
from src.api.routers.vitamins_name_vitamin_name import get_vitamin_by_name
from src.api.utils.operations_on_attributes import pop_attributes, add_attributes
from src.authentication.allowed_roles import admin_only
from src.database.supabase_connection import supabase_connection
from src.config import settings
from src.logger import logger


router = APIRouter()


@router.get("/ingredients", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.ingredient_table)
    return ingredients

@router.post("/ingredients", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def create_ingredient(ingredient: IngredientCreate):
    ingredient, poped_attributes = pop_attributes(ingredient, ["vitamins"])

    ingredient_response = supabase_connection.insert(
        settings.ingredient_table,
        ingredient,
    )
    logger.debug(f"ingredient_response: {ingredient_response}")

    ingredient_id = ingredient_response["id"]
    logger.debug(f"ingredient_id: {ingredient_id}")

    vitamins_response = []
    vitamins = poped_attributes[0]
    if vitamins:
        for vitamin in vitamins:
            try:
                exists = await get_vitamin_by_name(vitamin["name"])
            except:
                exists = None
                logger.error(f"vitamin: {vitamin["name"]} hasn't been recognized")
            if exists:
                logger.debug(f"exists: {exists}")

                supabase_connection.insert(
                    settings.vitamins_included_table,
                    {
                        "ingredient_id": ingredient_id,
                        "vitamin_id": exists["id"]
                    },
                )
                vitamins_response.append(exists)

    attributes = [{"vitamins": vitamins_response}]
    ingredient_response = add_attributes(
        ingredient_response,
        attributes
    )
    logger.debug(f"ingredient_response: {ingredient_response}")         

    return ingredient_response
