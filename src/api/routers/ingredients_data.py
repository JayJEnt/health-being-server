"""/ingredients_data_data router"""

from fastapi import APIRouter, Depends

from api.schemas.ingredient import IngredientDataCreate, IngredientDataResponse
from api.crud.crud_operations import CrudOperations
from api.authentication.allowed_roles import admin_only
from api.crud.utils import add_attributes


admin_router = APIRouter(
    prefix="/admin/ingredients_data", tags=["admin: ingredients_data"]
)
crud = CrudOperations("ingredients_data")


"""/admin/ingredients_data/{ingredient_id} endpoint"""


@admin_router.get(
    "/{ingredient_id}",
    response_model=IngredientDataResponse,
    dependencies=[Depends(admin_only)],
)
async def get_ingredient_data(ingredient_id: int):
    return await crud.get_by_id(ingredient_id)


# TODO: Move these endpoints to admin router and add proper validation
@admin_router.post(
    "/{ingredient_id}",
    response_model=IngredientDataResponse,
    dependencies=[Depends(admin_only)],
)
async def create_ingredient_data(ingredient_id: int, ingredient: IngredientDataCreate):
    ingredient = add_attributes(ingredient, [{"ingredient_id": ingredient_id}])
    return await crud.post(ingredient)


@admin_router.put(
    "/{ingredient_id}",
    response_model=IngredientDataResponse,
    dependencies=[Depends(admin_only)],
)
async def update_ingredient_data(ingredient_id: int, ingredient: IngredientDataCreate):
    return await crud.put(ingredient_id, ingredient)


@admin_router.delete(
    "/{ingredient_id}",
    response_model=IngredientDataResponse,
    dependencies=[Depends(admin_only)],
)
async def delete_ingredient_data(ingredient_id: int):
    return await crud.delete(ingredient_id)
