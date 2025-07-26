"""/recipes endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import CreateDetailedRecipe, Recipe, DetailedRecipe
from api.routers.diet_types_name_diet_name import get_diet_by_name
from api.routers.ingredients_name_ingredient_name import get_ingredient_by_name
from api.utils.operation_on_attributes import pop_attributes, add_attributes
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    recipes = supabase_connection.fetch_all(settings.recipe_table)
    return recipes

@router.post("/recipes/", response_model=DetailedRecipe)
async def create_recipe(recipe: CreateDetailedRecipe):
    recipe, poped_attributes = pop_attributes(recipe, ["diet_type", "ingredients"])

    recipe = supabase_connection.insert(
        settings.recipe_table,
        recipe,
    )
    logger.debug(f"recipe_response: {recipe}")

    recipe_response = recipe[0]
    recipe_id = recipe_response["id"]
    logger.debug(f"recipe_id: {recipe_id}")

    diet_type_response = []
    diet_type = poped_attributes[0]
    if diet_type:
        for diet in diet_type:
            exists = await get_diet_by_name(diet["diet_name"])
            if exists:
                logger.debug(f"exists: {exists}")
                diet_type_response.append(exists)
                supabase_connection.insert(
                    settings.diet_type_included_table,
                    {
                        "recipe_id": recipe_id,
                        "diet_type_id": exists["id"]
                    },
                )

    ingredients_response = []
    ingredients = poped_attributes[1]
    if ingredients:
        for ingredient in ingredients:
            exists = await get_ingredient_by_name(ingredient["name"])
            if exists:
                logger.debug(f"exists: {exists}")
                supabase_connection.insert(
                    settings.ingredients_included_table,
                    {
                        "recipe_id": recipe_id,
                        "ingredient_id": exists["id"],
                        "amount": ingredient["amount"],
                        "measure_unit": ingredient["measure_unit"]
                    },
                )
                attributes = [{"amount": ingredient["amount"]}, {"measure_unit": ingredient["measure_unit"]}]
                exists  = add_attributes(
                    exists,
                    attributes
                )
                ingredients_response.append(exists)
    attributes = [{"diet_type": diet_type_response}, {"ingredients": ingredients_response}]
    recipe_response = add_attributes(
        recipe_response,
        attributes
    )
    logger.debug(f"recipe_response: {recipe_response}")
    return recipe_response
