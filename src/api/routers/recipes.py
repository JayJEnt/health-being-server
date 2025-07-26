"""/recipes endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import CreateDetailedRecipe, Recipe, DetailedRecipe
from api.routers.diet_types_diet_name import get_diet_by_name
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger
from api.utils.extract_attributes import extract_attributes


router = APIRouter()


@router.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    recipes = supabase_connection.fetch_all(settings.recipe_table)
    return recipes

@router.post("/recipes/", response_model=DetailedRecipe)
async def create_recipe(recipe: CreateDetailedRecipe):
    recipe, diet_type_list = extract_attributes(recipe, ["diet_type"])
    diet_type = diet_type_list[0]

    recipe = supabase_connection.insert(
        settings.recipe_table,
        recipe,
    )
    logger.debug(f"recipe_response: {recipe}")

    recipe_id = recipe[0]["id"]
    logger.debug(f"recipe_id: {recipe_id}")

    if diet_type:
        for diet in diet_type:
            matching_diet = await get_diet_by_name(diet["diet_name"])
        # TODO: create endpoint for searching by name
        # existing_diet_types = supabase_connection.fetch_all(settings.diet_type_table)
        # logger.debug(f"existing_diet_types: {existing_diet_types}")

        # for diet in diet_type:
        #     for ex_diet in existing_diet_types:
        #         if ex_diet["diet_name"] == diet["diet_name"]:
        #             matching_diet = ex_diet
        #             break
            logger.debug(f"matching_diet: {matching_diet}")

            if matching_diet:
                supabase_connection.insert(
                    settings.diet_type_included_table,
                    {
                        "recipe_id": recipe_id,
                        "diet_type_id": matching_diet["id"]
                    },
                )
                logger.debug(f"sucessfully inserted: 'recipe_id': {recipe_id}, 'diet_type_id': {matching_diet['id']}")

    return recipe[0]
