"""/recipes router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.recipe import RecipePage, RecipeOverview, RecipePageResponse
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.utils.crud_operations import create_element, delete_element_by_id, get_element_by_id, get_element_by_name
from api.authentication.allowed_roles import logged_only
from api.handlers.exceptions import RescourceNotFound
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/recipes", tags=["recipes"])


"""/recipes endpoint"""
@router.get("", response_model=List[RecipeOverview])
async def get_recipes():
    recipes = supabase_connection.fetch_all(settings.RECIPE_TABLE)
    recipes_response = []
    for recipe in recipes:
        recipe, dropped_attributes = pop_attributes(recipe, ["description", "instructions"])
        recipes_response.append(recipe)
    return recipes_response

@router.post("", response_model=RecipePageResponse, dependencies=[Depends(logged_only)])
async def create_recipe(recipe: RecipePage):
    return await create_element("recipes", recipe)




"""/recipes/{recipe_id} endpoint"""
@router.get("/{recipe_id}", response_model=RecipePageResponse)
async def get_recipe(recipe_id: int):
    return await get_element_by_id("recipes", recipe_id)

@router.put("/{recipe_id}", response_model=RecipePageResponse)
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
                exists = await get_element_by_name("ingredients", ingredient["name"])
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

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int):
    return await delete_element_by_id("recipes", recipe_id)




"""/recipes/search/{phrase} endpoint"""
@router.get("/search/{phrase}", response_model=List[RecipeOverview])
# TODO: overall better searching mechanizm needed
async def search_for_matching_recipes(phrase: str):
    recipes = []

    try:
        found_by_title = supabase_connection.find_ilike(
            settings.RECIPE_TABLE,
            "title",
            phrase
        )
    except:
        found_by_title = None
    
    if found_by_title:
        recipes += found_by_title

    try:
        found_by_description = supabase_connection.find_ilike(
            settings.RECIPE_TABLE,
            "description",
            phrase
        )
    except:
        found_by_description = None

    if found_by_description:
        for recipe_found in found_by_description:
            duplicated = False
            for recipe in recipes:
                if recipe_found["id"] == recipe["id"]:
                    duplicated = True
                    break
            if not duplicated:
                recipes += recipe_found

    recipes_response = []
    for recipe in recipes:
        recipe, dropped_attributes = pop_attributes(recipe, ["description", "instructions"])
        recipes_response.append(recipe)
    return recipes_response
