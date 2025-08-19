"""/ingredients_data_data router"""
from fastapi import APIRouter, Depends

from api.schemas.ingredient import IngredientDataCreate, IngredientDataResponse
from api.crud.get_methods import get_element_by_id
from api.crud.post_methods import create_element
from api.crud.delete_methods import delete_element_by_id
from api.crud.put_methods import update_element_by_id
from api.authentication.allowed_roles import admin_only


router = APIRouter(prefix="/ingredients_data", tags=["ingredients_data"])


"""/ingredients_data/{ingredient_id} endpoint"""
@router.get("/{ingredient_id}", response_model=IngredientDataResponse)
async def get_ingredient_data(ingredient_id: int):
    return await get_element_by_id("ingredients_data", ingredient_id)

@router.put("/{ingredient_id}", response_model=IngredientDataResponse)
async def update_ingredient_data(ingredient_id: int, ingredient: IngredientDataCreate):
    return await update_element_by_id("ingredients_data", ingredient_id, ingredient)

@router.delete("/{ingredient_id}")
async def delete_ingredient_data(ingredient_id: int):
    return await delete_element_by_id("ingredients_data", ingredient_id)
