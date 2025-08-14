"""/recipes/{recipe_id} endpoint"""
from fastapi import APIRouter

from api.schemas.recipe import RecipePageResponse, RecipePage
from api.routers.ingredients_name_ingredient_name import get_ingredient_by_name
from api.utils.operations_on_attributes import add_attributes, pop_attributes
from api.utils.crud_operations import delete_element, get_element_by_id, get_element_by_name
from api.handlers.exceptions import RescourceNotFound
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/recipes/{recipe_id}", tags=["recipes"])


@router.get("", response_model=RecipePageResponse)
async def get_recipe(recipe_id: int):
    return await get_element_by_id("recipes", recipe_id)

@router.put("", response_model=RecipePageResponse)
async def update_recipe(recipe_id: int, recipe: RecipePage):
    recipe, poped_attributes = pop_attributes(recipe, ["diet_type", "ingredients"])
    recipe_response = supabase_connection.update_by(
        settings.RECIPE_TABLE,
        "id",
        recipe_id, 
        recipe,
    )
    logger.debug(f"Recipe_response: {recipe_response}.")

    try:
        supabase_connection.delete_by(
            settings.DIET_TYPE_INCLUDED_TABLE,
            "recipe_id",
            recipe_id,
        )
    except RescourceNotFound:
        pass

    try:
        diet_type_response = []
        diet_type = poped_attributes[0]
        if diet_type:
            for diet in diet_type:
                try:
                    exists = exists = await get_element_by_name("diet_type", diet["diet_name"])
                except RescourceNotFound:
                    exists = None
                    logger.error(f"Diet: {diet["diet_name"]} hasn't been recognized")
                if exists:
                    logger.debug(f"Exists: {exists}")

                    supabase_connection.insert(
                        settings.DIET_TYPE_INCLUDED_TABLE,
                        {
                            "recipe_id": recipe_id,
                            "diet_type_id": exists["id"]
                        },
                    )
                    diet_type_response.append(diet)
    except RescourceNotFound:
        pass

    try:
        supabase_connection.delete_by(
            settings.INGREDIENTS_INCLUDED_TABLE,
            "recipe_id",
            recipe_id,
        )
    except RescourceNotFound:
        pass

    ingredients_response = []
    ingredients = poped_attributes[1]
    if ingredients:
        for ingredient in ingredients:
            try:
                exists = await get_ingredient_by_name(ingredient["name"])
            except RescourceNotFound:
                exists = None
                logger.error(f"Ingredient: {ingredient["name"]} hasn't been recognized")
            if exists:
                logger.debug(f"Exists: {exists}")

                supabase_connection.insert(
                    settings.INGREDIENTS_INCLUDED_TABLE,
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
    attributes = ([{"diet_type": diet_type_response}, {"ingredients": ingredients_response}] 
                  if diet_type_response else [{"ingredients": ingredients_response}])
    recipe_response = add_attributes(
        recipe_response,
        attributes
    )
    logger.debug(f"recipe_response: {recipe_response}")

    return recipe_response

@router.delete("")
async def delete_recipe(recipe_id: int):
    return await delete_element("recipes", recipe_id)