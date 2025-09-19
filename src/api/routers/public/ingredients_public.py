"""/ingredients router"""

from fastapi import APIRouter

from typing import List

from api.crud.crud_operations import CrudOperations
from api.schemas.ingredient import Ingredient, IngredientResponse


router = APIRouter(prefix="/ingredients", tags=["public: ingredients"])
crud = CrudOperations("ingredients")


# TODO: Change to query params
@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    return await crud.get()


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await crud.get_all(
        ingredient_id,
        related_attributes=["vitamins"],
        nested_attributes=["ingredients_data"],
    )


@router.get("/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    return await crud.get_by_name(ingredient_name)
