"""/ingredients_data_data router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.crud.utils import add_attributes
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.ingredient import IngredientDataCreate, IngredientData


router = APIRouter(prefix="/ingredients_data", tags=["admin: ingredients_data"])
crud = CrudOperations("ingredients_data")


@router.get(
    "/",
    response_model=IngredientData,
    dependencies=[Depends(admin_only)],
)
async def get_ingredient_data(ingredient_id: int = None):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.get_by_id(ingredient_id)


@router.post(
    "/",
    response_model=IngredientData,
    dependencies=[Depends(admin_only)],
)
async def create_ingredient_data(
    ingredient: IngredientDataCreate, ingredient_id: int = None
):
    if not ingredient_id:
        raise DemandQueryParameter
    ingredient = add_attributes(ingredient, [{"ingredient_id": ingredient_id}])
    return await crud.post(ingredient)


@router.put(
    "/",
    response_model=IngredientData,
    dependencies=[Depends(admin_only)],
)
async def update_ingredient_data(
    ingredient: IngredientDataCreate, ingredient_id: int = None
):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.put(ingredient_id, ingredient)


@router.delete(
    "/",
    response_model=IngredientData,
    dependencies=[Depends(admin_only)],
)
async def delete_ingredient_data(ingredient_id: int = None):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.delete(ingredient_id)
