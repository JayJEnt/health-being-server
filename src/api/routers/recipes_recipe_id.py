"""/recipes/{recipe_id} endpoint"""
from fastapi import APIRouter

from api.schemas.recipe import RecipeBaseModel, Recipe
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()

# TODO: user has to recive RecipeResponse instead of Recipe
@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    recipe = supabase_connection.find_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    return recipe

# TODO: user should be able to change entire page, input model RecipePage instead of RecipeBaseModel and RecipePage instead of Recipe
# Should be able to moderate relationships, if he removes diet_type, or ingredient from recipe
# -> diet_type_included, ingredients_included
@router.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe: RecipeBaseModel):
    recipe = supabase_connection.update_by(
        settings.recipe_table,
        "id",
        recipe_id, 
        recipe.model_dump(),
    )
    return recipe

@router.delete("/recipes/{recipe_id}")
# TODO: should delete as well all related rows in:
# diet_type_included, ingredients_included
async def delete_recipe(recipe_id: int):
    recipe = supabase_connection.delete_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    return recipe