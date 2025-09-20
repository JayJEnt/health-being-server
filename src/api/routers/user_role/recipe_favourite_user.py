"""/recipe_favourite router"""

from fastapi import APIRouter, Depends

from typing import List, Union

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.recipe_favourite import (
    RecipeFavouriteCreate,
    RecipeFavouriteResponse,
    RecipeFavouriteDelete,
)
from api.schemas.recipe import Recipe
from api.schemas.user import User


router = APIRouter(prefix="/recipe_favourite", tags=["user: recipe_favourite"])
crud = CrudOperations("user")


@router.get(
    "",
    response_model=Union[RecipeFavouriteResponse, List[RecipeFavouriteResponse]],
    dependencies=[Depends(logged_only)],
)
async def get_relation_recipe_favourite(
    recipe_id: int = None, requesting_user: User = Depends(validate_token)
):
    if recipe_id:
        return await crud.get_relationship(
            requesting_user.id, "recipes", recipe_id, find_name=True
        )
    return await crud.get_relationships(requesting_user.id, "recipes", find_name=True)


@router.post(
    "",
    response_model=Recipe,
    dependencies=[Depends(logged_only)],
)
async def create_relation_recipe_favourite(
    recipe: RecipeFavouriteCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "recipes", recipe)


@router.delete(
    "", response_model=RecipeFavouriteDelete, dependencies=[Depends(logged_only)]
)
async def delete_relation_recipe_favourite(
    recipe_id: int, requesting_user: User = Depends(validate_token)
):
    return await crud.delete_relationship(requesting_user.id, "recipes", recipe_id)
