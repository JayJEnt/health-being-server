"""/ingredients_data_data router"""
from fastapi import APIRouter, Depends

from api.schemas.ingredient import IngredientDataCreate, IngredientDataResponse
from api.crud.single_entity.get_methods import get_element_by_id
from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.delete_methods import delete_element_by_id
from api.crud.single_entity.put_methods import update_element_by_id
from api.authentication.allowed_roles import admin_only
from api.crud.utils import add_attributes


admin_router = APIRouter(prefix="/admin/ingredients_data", tags=["admin: ingredients_data"])


"""/admin/ingredients_data/{ingredient_id} endpoint"""
@admin_router.get("/{ingredient_id}", response_model=IngredientDataResponse, dependencies=[Depends(admin_only)])
async def get_ingredient_data(ingredient_id: int):
    return await get_element_by_id("ingredients_data", ingredient_id)


@admin_router.post("/{ingredient_id}", response_model=IngredientDataResponse, dependencies=[Depends(admin_only)])
async def get_ingredient_data(ingredient_id: int, ingredient: IngredientDataCreate):
    ingredient = add_attributes(ingredient, [{"ingredient_id": ingredient_id}])
    return await create_element("ingredients_data", ingredient)


@admin_router.put("/{ingredient_id}", response_model=IngredientDataResponse, dependencies=[Depends(admin_only)])
async def update_ingredient_data(ingredient_id: int, ingredient: IngredientDataCreate):
    return await update_element_by_id("ingredients_data", ingredient_id, ingredient)


@admin_router.delete("/{ingredient_id}", dependencies=[Depends(admin_only)])
async def delete_ingredient_data(ingredient_id: int):
    return await delete_element_by_id("ingredients_data", ingredient_id)
