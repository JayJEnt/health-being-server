"""/recipes router"""

from fastapi import APIRouter, Depends

from typing import List

from api.authentication.allowed_roles import logged_only, owner_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.crud.utils import add_attributes
from api.schemas.recipe import RecipeCreate, Recipe, RecipeResponse, RecipeOverview
from api.schemas.filters import RecipeFilter
from api.schemas.user import User


router = APIRouter(prefix="/recipes", tags=["user: recipes"])
crud = CrudOperations("recipes")


@router.post("", response_model=RecipeResponse, dependencies=[Depends(logged_only)])
async def create_recipe(
    recipe: RecipeCreate, requesting_user: User = Depends(validate_token)
):
    recipe = add_attributes(recipe, [{"owner_id": requesting_user.id}])
    return await crud.post_all(recipe, related_attributes=["ingredients", "diet_type"])


@router.put("", response_model=RecipeResponse, dependencies=[Depends(logged_only)])
async def update_recipe(
    recipe: RecipeCreate,
    recipe_id: int,
    requesting_user: User = Depends(validate_token),
):
    await owner_only("recipes", recipe_id, requesting_user)

    return await crud.put_all(
        recipe_id, recipe, related_attributes=["ingredients", "diet_type"]
    )


@router.delete("", response_model=Recipe, dependencies=[Depends(logged_only)])
async def delete_recipe(
    recipe_id: int, requesting_user: User = Depends(validate_token)
):
    await owner_only("recipes", recipe_id, requesting_user)

    return await crud.delete_all(
        recipe_id, related_attributes=["ingredients", "diet_type"]
    )


@router.post(
    "/deep_search",
    response_model=List[RecipeOverview],
    dependencies=[Depends(logged_only)],
)
async def get_recipes(
    filters: RecipeFilter, phrase: str, requesting_user: User = Depends(validate_token)
):
    return await crud.search(
        phrase, filters.model_dump(), requesting_user.id, restrict=True
    )
