"""/recipes/search/{phrase} endpoint"""
from fastapi import APIRouter

from typing import List, Optional

from api.schemas.recipe import RecipeOverview, Recipe
from api.utils.operations_on_attributes import pop_attributes
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter(prefix="/recipes/search/{phrase}", tags=["recipes"])


@router.get("", response_model=List[RecipeOverview])
# TODO: overall better searching mechanizm needed
async def search_for_matching_recipes(phrase: str):
    recipes = []

    found_by_title = find_by_title(phrase)
    if found_by_title:
        recipes += found_by_title

    found_by_description = find_by_description(phrase)
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

def find_by_title(phrase: str) -> Optional[List[Recipe]]:
    try:
        return supabase_connection.find_ilike(
            settings.RECIPE_TABLE,
            "title",
            phrase
        )
    except:
        return None
    
def find_by_description(phrase: str) -> Optional[List[Recipe]]:
    try:
        return supabase_connection.find_ilike(
            settings.RECIPE_TABLE,
            "description",
            phrase
        )
    except:
        return None