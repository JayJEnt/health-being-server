"""/recipes endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import CreateRecipe, Recipe
from db_conn import supabase_connection
from config import settings


router = APIRouter()


@router.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    recipes = supabase_connection.fetch_all(settings.recipe_table)
    return recipes

@router.post("/recipes/", response_model=List[Recipe])
async def create_recipe(recipe: CreateRecipe):
    recipe = supabase_connection.insert(
        settings.recipe_table,
        recipe.model_dump(),
    )
    return recipe
