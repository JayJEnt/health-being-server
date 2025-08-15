"""/ingredients router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse
from api.utils.crud_operations import create_element, delete_element_by_id, get_element_by_id, get_element_by_name
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.authentication.allowed_roles import admin_only
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


"""/ingredients endpoint"""
@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.INGREDIENT_TABLE)
    return ingredients

@router.post("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def create_ingredient(ingredient: IngredientCreate):
    return await create_element("ingredients", ingredient)




"""/ingredients/{ingredient_id} endpoint"""
@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await get_element_by_id("ingredients", ingredient_id)

@router.put("/{ingredient_id}", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
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

@router.delete("/{ingredient_id}", dependencies=[Depends(admin_only)])
async def delete_ingredient(ingredient_id: int):
    return await delete_element_by_id("ingredients", ingredient_id)




"""/ingredients/name/{ingredient_name} endpoint"""
@router.get("/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    ingredient = supabase_connection.find_ilike(
        settings.INGREDIENT_TABLE,
        "name",
        ingredient_name,
    )
    return ingredient[0]