"""/ingredients router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.schemas.ingredient import IngredientCreate, IngredientResponseAll


router = APIRouter(prefix="/ingredients", tags=["admin: ingredients"])
crud = CrudOperations("ingredients")


@router.post(
    "", response_model=IngredientResponseAll, dependencies=[Depends(admin_only)]
)
async def create_ingredient(ingredient: IngredientCreate):
    return await crud.post_all(
        ingredient,
        related_attributes=["vitamins"],
    )


@router.put(
    "",
    response_model=IngredientResponseAll,
    dependencies=[Depends(admin_only)],
)
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    return await crud.put_all(
        ingredient_id,
        ingredient,
        related_attributes=["vitamins"],
    )


# TEMP FIX 25/08/2025
crud2 = CrudOperations("refrigerator")


@router.delete(
    "",
    response_model=IngredientResponseAll,
    dependencies=[Depends(admin_only)],
)
async def delete_ingredient(ingredient_id: int):
    await crud2.delete_relationships(ingredient_id, ["user"])  # TEMP FIX 25/08/2025
    return await crud.delete_all(
        ingredient_id,
        related_attributes=[
            "vitamins",
            "user",
            "recipes",
        ],  # TODO: FIX misses refrigerator table TEMP FIX 25/08/2025
    )
