"""/ingredients/{ingredient_id} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.ingredient import IngredientCreate, IngredientResponse
from api.routers.vitamins_name_vitamin_name import get_vitamin_by_name
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from authentication.allowed_roles import admin_only
from api.handlers.exceptions import RescourceNotFound
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/ingredients/{ingredient_id}", tags=["ingredients"])


@router.get("", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    ingredient_response = supabase_connection.find_by(
        settings.ingredient_table,
        "id",
        ingredient_id,
    )

    try:
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
    except RescourceNotFound:
        logger.info("There were no linked vitamins to this ingredient")
    return ingredient_response

@router.put("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
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

@router.delete("", dependencies=[Depends(admin_only)])
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