"""/prefered_recipe_type router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.prefered_recipe_type import (
    PreferedRecipeTypeCreate,
    PreferedRecipeTypeDelete,
    PreferedRecipeTypeResponse,
    PreferedRecipeTypeCreateResponse,
)
from api.schemas.user import User


router = APIRouter(prefix="/prefered_recipe_type", tags=["user: prefered_recipe_type"])
crud = CrudOperations("user")


@router.get(
    "",
    response_model=list[PreferedRecipeTypeResponse],
    dependencies=[Depends(logged_only)],
)
async def get_all_relations_prefered_recipe_type(
    requesting_user: User = Depends(validate_token),
):
    return await crud.get_relationships(requesting_user.id, "diet_type", find_name=True)


@router.post(
    "",
    response_model=PreferedRecipeTypeCreateResponse,
    dependencies=[Depends(logged_only)],
)
async def create_relation_prefered_recipe_type(
    diet_type: PreferedRecipeTypeCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "diet_type", diet_type)


@router.get(
    "/", response_model=PreferedRecipeTypeResponse, dependencies=[Depends(logged_only)]
)
async def get_relation_prefered_recipe_type(
    diet_type_id: int, requesting_user: User = Depends(validate_token)
):
    if not diet_type_id:
        raise DemandQueryParameter
    return await crud.get_relationship(
        requesting_user.id, "diet_type", diet_type_id, find_name=True
    )


@router.delete(
    "/", response_model=PreferedRecipeTypeDelete, dependencies=[Depends(logged_only)]
)
async def delete_relation_prefered_recipe_type(
    diet_type_id: int, requesting_user: User = Depends(validate_token)
):
    if not diet_type_id:
        raise DemandQueryParameter
    return await crud.delete_relationship(requesting_user.id, "diet_type", diet_type_id)
