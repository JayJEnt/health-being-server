"""/recipes/search/{phrase} endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.recipe import Recipe
from database.supabase_connection import supabase_connection
from config import settings


router = APIRouter()


@router.get("/recipes/search/{phrase}", response_model=List[Recipe])
async def search_for_matching_recipes(phrase: str):
    recipes = supabase_connection.find_by(
        settings.recipe_table,
        "title",
        phrase
    )
    recipes += supabase_connection.find_by(
        settings.recipe_table,
        "description",
        phrase
    )
    return recipes