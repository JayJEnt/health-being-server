"""/ingredients/{ingredient_id} endpoint"""
from fastapi import APIRouter, Depends

from api.schemas.ingredient import IngredientCreate, IngredientResponse
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.utils.crud_operations import delete_element, get_element_by_id, get_element_by_name
from authentication.allowed_roles import admin_only
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/ingredients/{ingredient_id}", tags=["ingredients"])


@router.get("", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await get_element_by_id("ingredients", ingredient_id)

@router.put("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    ingredient, poped_attributes = pop_attributes(ingredient, ["vitamins"])
    ingredient_response = supabase_connection.update_by(
        settings.INGREDIENT_TABLE,
        "id",
        ingredient_id, 
        ingredient,
    )
    logger.debug(f"Ingredient_response: {ingredient_response}.")

    supabase_connection.delete_by(
        settings.VITAMINS_INCLUDED_TABLE,
        "ingredient_id",
        ingredient_id,
    )

    vitamins_response = []
    vitamins = poped_attributes[0]
    if vitamins:
        for vitamin in vitamins:
            try:
                exists = await get_element_by_name("vitamins", vitamin["name"])
            except:
                exists = None
                logger.error(f"Vitamin: {vitamin["name"]} hasn't been recognized.")
            if exists:
                logger.debug(f"Exists: {exists}.")

                supabase_connection.insert(
                    settings.VITAMINS_INCLUDED_TABLE,
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
    return await delete_element("ingredients", ingredient_id)