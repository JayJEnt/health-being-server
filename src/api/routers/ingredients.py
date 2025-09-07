"""/ingredients router"""

from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.schemas.ingredient import IngredientCreate, Ingredient, IngredientResponse


router = APIRouter(prefix="/ingredients", tags=["ingredients"])
crud = CrudOperations("ingredients")


"""/ingredients endpoint"""


@router.get("", response_model=List[Ingredient])
async def get_ingredients():
    return await crud.get()


"""/ingredients/{ingredient_id} endpoint"""


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int):
    return await crud.get_all(
        ingredient_id,
        related_attributes=["vitamins"],
        nested_attributes=["ingredients_data"],
    )


"""/ingredients/name/{ingredient_name} endpoint"""


@router.get("/name/{ingredient_name}", response_model=Ingredient)
async def get_ingredient_by_name(ingredient_name: str):
    return await crud.get_by_name(ingredient_name)


admin_router = APIRouter(prefix="/admin/ingredients", tags=["admin: ingredients"])


"""/admin/ingredients endpoint"""


@admin_router.post(
    "", response_model=IngredientResponse, dependencies=[Depends(admin_only)]
)
async def create_ingredient(ingredient: IngredientCreate):
    return await crud.post_all(
        ingredient,
        related_attributes=["vitamins"],
        nested_attributes=["ingredients_data"],
    )


"""/admin/ingredients/{ingredient_id} endpoint"""


@admin_router.put(
    "/{ingredient_id}",
    response_model=IngredientResponse,
    dependencies=[Depends(admin_only)],
)
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    return await crud.put_all(
        ingredient_id,
        ingredient,
        related_attributes=["vitamins"],
        nested_attributes=["ingredients_data"],
    )


# TEMP FIX 25/08/2025
crud2 = CrudOperations("refrigerator")


@admin_router.delete("/{ingredient_id}", dependencies=[Depends(admin_only)])
async def delete_ingredient(ingredient_id: int):
    await crud2.delete_relationships(ingredient_id, ["user"])  # TEMP FIX 25/08/2025
    return await crud.delete_all(
        ingredient_id,
        related_attributes=["vitamins", "user"],  # TODO: FIX misses refrigerator table
        nested_attributes=["ingredients_data"],
    )
