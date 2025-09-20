"""/recipes router"""

from fastapi import APIRouter

from typing import List

from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.recipe import RecipeOverview, RecipeResponse


router = APIRouter(prefix="/recipes", tags=["public: recipes"])
crud = CrudOperations("recipes")


@router.get("", response_model=List[RecipeOverview])
async def get_recipes(phrase: str = None):
    if phrase:
        return await crud.search(phrase, restrict=True)
    return await crud.get(restrict=True)


@router.get("/", response_model=RecipeResponse)
async def get_recipe(recipe_id: int = None):
    if not recipe_id:
        raise DemandQueryParameter
    return await crud.get_all(
        recipe_id, related_attributes=["ingredients", "diet_type"]
    )
