"""/recipes/search/{phrase} endpoint"""
from fastapi import APIRouter

from typing import List, Optional

from api.schemas.recipe import RecipeOverview, Recipe
from api.utils.operations_on_attributes import pop_attributes
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/recipes/search/{phrase}", response_model=List[RecipeOverview])
# TODO: overall better searching mechanizm needed
async def search_for_matching_recipes(phrase: str):
    recipes = []
    
    # TODO: [OPTIMALIZATION] Consider running async
    found_by_title = find_by_title(phrase)
    if found_by_title:
        recipes += found_by_title

    # TODO: [OPTIMALIZATION] Consider running async
    found_by_description = find_by_description(phrase)
    if found_by_description:
        recipes += found_by_description

    recipes_response = []
    for recipe in recipes:
        recipe, dropped_attributes = pop_attributes(recipe, ["description", "instructions"])
        recipes_response.append(recipe)
    return recipes_response

def find_by_title(phrase: str) -> Optional[List[Recipe]]:
    try:
        return supabase_connection.find_by(
            settings.recipe_table,
            "title",
            phrase
        )
    except:
        return None
    
def find_by_description(phrase: str) -> Optional[List[Recipe]]:
    try:
        return supabase_connection.find_by(
            settings.recipe_table,
            "description",
            phrase
        )
    except:
        return None
    

# TODO: add ilike/like search method