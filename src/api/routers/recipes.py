"""/recipes endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.recipe import RecipePage, RecipeOverview, RecipePageResponse
from api.utils.operations_on_attributes import pop_attributes
from api.utils.crud_operations import create_element
from authentication.allowed_roles import logged_only
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/recipes", tags=["recipes"])


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
