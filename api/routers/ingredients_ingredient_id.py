"""/ingredients/{ingredient_id} endpoint"""
from fastapi import APIRouter

from typing import List

from api.schemas.ingredient import CreateIngredient, Ingredient
from db_conn import supabase_connection
from config import settings


router = APIRouter()


@router.get("/ingredients/{ingredient_id}", response_model=List[Ingredient])
async def get_ingredient(ingredient_id: int):
    ingredient = supabase_connection.find_by(
        settings.ingredient_table,
        "id",
        ingredient_id,
    )
    return ingredient

@router.put("/ingredients/{ingredient_id}", response_model=List[Ingredient])
async def update_ingredient(ingredient_id: int, ingredient: CreateIngredient):
    ingredient = supabase_connection.update_by(
        settings.ingredient_table,
        "id",
        ingredient_id, 
        ingredient.model_dump(),
    )
    return ingredient

@router.delete("/ingredients/{ingredient_id}")
async def delete_ingredient(ingredient_id: int):
    ingredient = supabase_connection.delete_by(
        settings.ingredient_table,
        "id",
        ingredient_id,
    )
    return ingredient