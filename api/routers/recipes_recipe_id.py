"""/recipes/{recipe_id} endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import CreateRecipe, Recipe
from db_conn import supabase_connection
from config import settings


router = APIRouter()


@router.get("/recipes/{recipe_id}", response_model=List[Recipe])
async def get_recipe(recipe_id: int):
    recipe = supabase_connection.find_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    return recipe

@router.put("/recipes/{recipe_id}", response_model=List[Recipe])
async def update_recipe(recipe_id: int, recipe: CreateRecipe):
    recipe = supabase_connection.update_by(
        settings.recipe_table,
        "id",
        recipe_id, 
        recipe.model_dump(),
    )
    return recipe

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    recipe = supabase_connection.delete_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    return recipe