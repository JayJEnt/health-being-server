"""/recipe_favourite router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.recipe_favourite import (
    RecipeFavouriteCreate,
    RecipeFavouriteCreateResponse,
    RecipeFavouriteResponse,
    RecipeFavouriteDelete,
)
from api.schemas.user import User


router = APIRouter(prefix="/recipe_favourite", tags=["user: recipe_favourite"])
crud = CrudOperations("user")


@router.get(
    "",
    response_model=list[RecipeFavouriteResponse],
    dependencies=[Depends(logged_only)],
)
async def get_all_relations_recipe_favourite(
    requesting_user: User = Depends(validate_token),
):
    return await crud.get_relationships(requesting_user.id, "recipes", find_name=True)


@router.post(
    "",
    response_model=RecipeFavouriteCreateResponse,
    dependencies=[Depends(logged_only)],
)
async def create_relation_recipe_favourite(
    recipe: RecipeFavouriteCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "recipes", recipe)


@router.get(
    "/", response_model=RecipeFavouriteResponse, dependencies=[Depends(logged_only)]
)
async def get_relation_recipe_favourite(
    recipe_id: int, requesting_user: User = Depends(validate_token)
):
    if not recipe_id:
        raise DemandQueryParameter
    return await crud.get_relationship(
        requesting_user.id, "recipes", recipe_id, find_name=True
    )


@router.delete(
    "/", response_model=RecipeFavouriteDelete, dependencies=[Depends(logged_only)]
)
async def delete_relation_recipe_favourite(
    recipe_id: int, requesting_user: User = Depends(validate_token)
):
    if not recipe_id:
        raise DemandQueryParameter
    return await crud.delete_relationship(requesting_user.id, "recipes", recipe_id)
