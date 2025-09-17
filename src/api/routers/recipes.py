"""/recipes router"""

from fastapi import APIRouter, Depends

from typing import List

from api.schemas.recipe import RecipeCreate, RecipeOverview, RecipeResponse
from api.schemas.user import UserResponse
from api.crud.crud_operations import CrudOperations
from api.crud.utils import add_attributes
from api.authentication.allowed_roles import logged_only, owner_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/recipes", tags=["recipes"])
crud = CrudOperations("recipes")


"""/recipes endpoint"""


@router.get("", response_model=List[RecipeOverview])
async def get_recipes():
    return await crud.get(True)


@router.post("", response_model=RecipeResponse, dependencies=[Depends(logged_only)])
async def create_recipe(
    recipe: RecipeCreate, requesting_user: UserResponse = Depends(validate_token)
):
    recipe = add_attributes(recipe, [{"owner_id": requesting_user.id}])
    return await crud.post_all(recipe, related_attributes=["ingredients", "diet_type"])


"""/recipes/{recipe_id} endpoint"""


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int):
    return await crud.get_all(
        recipe_id, related_attributes=["ingredients", "diet_type"]
    )


@router.put(
    "/{recipe_id}", response_model=RecipeResponse, dependencies=[Depends(logged_only)]
)
async def update_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    requesting_user: UserResponse = Depends(validate_token),
):
    await owner_only("recipes", recipe_id, requesting_user)

    return await crud.put_all(
        recipe_id, recipe, related_attributes=["ingredients", "diet_type"]
    )


@router.delete("/{recipe_id}", dependencies=[Depends(logged_only)])
async def delete_recipe(
    recipe_id: int, requesting_user: UserResponse = Depends(validate_token)
):
    await owner_only("recipes", recipe_id, requesting_user)

    return await crud.delete_all(
        recipe_id, related_attributes=["ingredients", "diet_type"]
    )


"""/recipes/search/{phrase} endpoint"""


@router.get("/search/{phrase}", response_model=List[RecipeOverview])
async def search_recipes(phrase: str):
    return await crud.search(phrase, True)


admin_router = APIRouter(prefix="/admin/recipes", tags=["admin: recipes"])


# TODO: Add admin routers
