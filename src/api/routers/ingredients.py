"""/ingredients router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse, IngredientUpdate, IngredientUpdateResponse
from api.crud.single_entity.get_methods import get_elements, get_element_by_name
from api.crud.entity_all_attached.get_methods import get_element_by_id
from api.crud.entity_all_attached.post_methods import create_element
from api.crud.entity_all_attached.delete_methods import delete_element_by_id
from api.crud.entity_with_relations.put_methods import update_element_by_id
from api.authentication.allowed_roles import admin_only


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


"""/ingredients endpoint"""
@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    return await get_elements("ingredients")




"""/ingredients/{ingredient_id} endpoint"""
@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await get_element_by_id("ingredients", ingredient_id)




"""/ingredients/name/{ingredient_name} endpoint"""
@router.get("/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    return await get_element_by_name("ingredients", ingredient_name)




admin_router = APIRouter(prefix="/admin/ingredients", tags=["admin: ingredients"])


"""/admin/ingredients endpoint"""
@admin_router.post("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def create_ingredient(ingredient: IngredientCreate):
    return await create_element("ingredients", ingredient)




"""/admin/ingredients/{ingredient_id} endpoint"""
@admin_router.put("/{ingredient_id}", response_model=IngredientUpdateResponse, dependencies=[Depends(admin_only)])
async def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate):
    return await update_element_by_id("ingredients", ingredient_id, ingredient)


@admin_router.delete("/{ingredient_id}", dependencies=[Depends(admin_only)])
async def delete_ingredient(ingredient_id: int):
    return await delete_element_by_id("ingredients", ingredient_id)