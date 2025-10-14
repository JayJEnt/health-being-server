"""/ingredients router"""

from fastapi import APIRouter

from typing import List, Union

from api.crud.crud_operations import CrudOperations
from api.schemas.ingredient import IngredientResponse


router = APIRouter(prefix="/ingredients", tags=["public: ingredients"])
crud = CrudOperations("ingredients")


@router.get("", response_model=Union[IngredientResponse, List[IngredientResponse]])
async def get_ingredients(
    ingredient_id: int = None, ingredient_name: str = None, search_phrase: str = None
):
    if ingredient_id:
        return await crud.get_by_id(ingredient_id)
    if ingredient_name:
        return await crud.get_by_name(ingredient_name)
    if search_phrase:
        return await crud.search(search_phrase)
    return await crud.get()
