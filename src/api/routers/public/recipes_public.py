"""/recipes router"""

from fastapi import APIRouter

from typing import List, Union

from api.crud.crud_operations import CrudOperations
from api.schemas.recipe import RecipeOverview, RecipeResponse


router = APIRouter(prefix="/recipes", tags=["public: recipes"])
crud = CrudOperations("recipes")


@router.get("", response_model=Union[RecipeResponse, List[RecipeOverview]])
async def get_recipes(recipe_id: int = None, phrase: str = None):
    if recipe_id:
        return await crud.get_all(
            recipe_id, related_attributes=["ingredients", "diet_type"]
        )
    if phrase:
        return await crud.search(phrase, restrict=True)
    return await crud.get(restrict=True)
