"""/ingredients router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse
from api.crud.crud_operator import (
    get_elements,
    create_element,
    delete_element_by_id,
    update_element_by_id,
    get_element_by_id,
    get_element_by_name,
)
from api.authentication.allowed_roles import admin_only


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


"""/ingredients endpoint"""
@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    return await get_elements("ingredients")

@router.post("", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def create_ingredient(ingredient: IngredientCreate):
    return await create_element("ingredients", ingredient)




"""/ingredients/{ingredient_id} endpoint"""
@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await get_element_by_id("ingredients", ingredient_id)

@router.put("/{ingredient_id}", response_model=IngredientResponse, dependencies=[Depends(admin_only)])
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    return await update_element_by_id("ingredients", ingredient_id, ingredient)

@router.delete("/{ingredient_id}", dependencies=[Depends(admin_only)])
async def delete_ingredient(ingredient_id: int):
    return await delete_element_by_id("ingredients", ingredient_id)




"""/ingredients/name/{ingredient_name} endpoint"""
@router.get("/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    return await get_element_by_name("ingredients", ingredient_name)