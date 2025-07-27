"""/recipes endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import RecipePage, RecipeOverview, RecipePageResponse
from api.routers.diet_types_name_diet_name import get_diet_by_name
from api.routers.ingredients_name_ingredient_name import get_ingredient_by_name
from api.utils.operation_on_attributes import pop_attributes, add_attributes
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/recipes/", response_model=List[RecipeOverview])
async def get_recipes():
    recipes = supabase_connection.fetch_all(settings.recipe_table)
    recipes_response = []
    for recipe in recipes:
        recipe, dropped_attributes = pop_attributes(recipe, ["description", "instructions"])
        recipes_response.append(recipe)
    return recipes_response

@router.post("/recipes/", response_model=RecipePageResponse)
async def create_recipe(recipe: RecipePage):
    recipe, poped_attributes = pop_attributes(recipe, ["diet_type", "ingredients"])

    recipe_response = supabase_connection.insert(
        settings.recipe_table,
        recipe,
    )
    logger.debug(f"Recipe_response: {recipe_response}")

    recipe_id = recipe_response["id"]
    logger.debug(f"Recipe_id: {recipe_id}")

    diet_type_response = []
    diet_type = poped_attributes[0]
    if diet_type:
        for diet in diet_type:
            try:
                exists = exists = await get_diet_by_name(diet["diet_name"])
            except:
                exists = None
                logger.error(f"Diet: {diet["diet_name"]} hasn't been recognized")
            if exists:
                logger.debug(f"Exists: {exists}")

                supabase_connection.insert(
                    settings.diet_type_included_table,
                    {
                        "recipe_id": recipe_id,
                        "diet_type_id": exists["id"]
                    },
                )
                diet_type_response.append(diet)

    ingredients_response = []
    ingredients = poped_attributes[1]
    if ingredients:
        for ingredient in ingredients:
            try:
                exists = await get_ingredient_by_name(ingredient["name"])
            except:
                exists = None
                logger.error(f"Ingredient: {ingredient["name"]} hasn't been recognized")
            if exists:
                logger.debug(f"Exists: {exists}")

                supabase_connection.insert(
                    settings.ingredients_included_table,
                    {
                        "recipe_id": recipe_id,
                        "ingredient_id": exists["id"],
                        "amount": ingredient["amount"],
                        "measure_unit": ingredient["measure_unit"]
                    },
                )
                ingredients_response.append(ingredient)

    if not ingredients_response:
        logger.error("There are no valid ingredients in this recipe.")
    attributes = [{"diet_type": diet_type_response}, {"ingredients": ingredients_response}]
    recipe_response = add_attributes(
        recipe_response,
        attributes
    )
    logger.debug(f"recipe_response: {recipe_response}")

    return recipe_response
