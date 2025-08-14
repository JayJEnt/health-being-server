"""/ingredients endpoint"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse
from api.utils.crud_operations import create_element
from authentication.allowed_roles import admin_only
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    ingredients = supabase_connection.fetch_all(settings.INGREDIENT_TABLE)
    return ingredients

@router.post("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def create_ingredient(ingredient: IngredientCreate):
    return await create_element("ingredients", ingredient)