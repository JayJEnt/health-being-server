"""/ingredients/{ingredient_id} endpoint"""
from fastapi import APIRouter

from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse
from api.routers.vitamins_name_vitamin_name import get_vitamin_by_name
from api.utils.operation_on_attributes import pop_attributes, add_attributes
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    ingredient_response = supabase_connection.find_by(
        settings.ingredient_table,
        "id",
        ingredient_id,
    )

    vitamins_included = supabase_connection.find_by(
        settings.vitamins_included_table,
        "ingredient_id",
        ingredient_id,
    )
    vitamins_response = []
    if vitamins_included:
        for vitamin_included in vitamins_included:
            vitamin_id = vitamin_included["vitamin_id"]
            logger.debug(f"vitamin_id: {vitamin_id}")

            vitamin = supabase_connection.find_by(
                settings.vitamin_table,
                "id",
                vitamin_id,
            )

            vitamin_name = vitamin[0]["name"]
            logger.debug(f"vitamin_name: {vitamin_name}")
            vitamins_response.append({
                "name": vitamin_name,
                "id": vitamin_id
            })

    attributes = [{"vitamins": vitamins_response}]
    ingredient_response = add_attributes(
        ingredient_response[0],
        attributes
    )
    return ingredient_response

# TODO: add role validation -> only for admin
@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    ingredient, poped_attributes = pop_attributes(ingredient, ["vitamins"])
    ingredient_response = supabase_connection.update_by(
        settings.ingredient_table,
        "id",
        ingredient_id, 
        ingredient,
    )
    logger.debug(f"Ingredient_response: {ingredient_response}.")

    supabase_connection.delete_by(
        settings.vitamins_included_table,
        "ingredient_id",
        ingredient_id,
    )

    vitamins_response = []
    vitamins = poped_attributes[0]
    if vitamins:
        for vitamin in vitamins:
            try:
                exists = await get_vitamin_by_name(vitamin["name"])
            except:
                exists = None
                logger.error(f"Vitamin: {vitamin["name"]} hasn't been recognized.")
            if exists:
                logger.debug(f"Exists: {exists}.")

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
    logger.debug(f"Ingredient_response: {ingredient_response}.")

    return ingredient_response

# TODO: add role validation -> only for admin
@router.delete("/ingredients/{ingredient_id}")
async def delete_ingredient(ingredient_id: int):
    supabase_connection.delete_by(
        settings.vitamins_included_table,
        "ingredient_id",
        ingredient_id,
    )

    ingredient = supabase_connection.delete_by(
        settings.ingredient_table,
        "id",
        ingredient_id,
    )
    return ingredient