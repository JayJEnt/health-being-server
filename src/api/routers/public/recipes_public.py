"""/recipes router"""

from fastapi import APIRouter

from typing import List, Union

from api.crud.crud_operations import CrudOperations
from api.recipe_metrics.micronutrients_summary import update_recipe_with_micronutrients
from api.schemas.recipe import RecipeOverview, RecipeResponseGet


router = APIRouter(prefix="/recipes", tags=["public: recipes"])
crud = CrudOperations("recipes")


@router.get("", response_model=Union[RecipeResponseGet, List[RecipeOverview]])
async def get_recipes(recipe_id: int = None, phrase: str = None):
    if recipe_id:
        recipe = await crud.get_all(
            recipe_id, related_attributes=["ingredients", "diet_type"]
        )
        return await update_recipe_with_micronutrients(recipe)
    if phrase:
        return await crud.search(phrase, restrict=True)
    return await crud.get(restrict=True)
