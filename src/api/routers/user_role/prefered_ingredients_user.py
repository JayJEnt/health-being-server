"""/prefered_ingredients router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.prefered_ingredients import (
    PreferedIngredientsCreate,
    PreferedIngredientsDelete,
    PreferedIngredientsResponse,
    PreferedIngredientsCreateResponse,
)
from api.schemas.user import User


router = APIRouter(prefix="/prefered_ingredients", tags=["user: prefered_ingredients"])
crud = CrudOperations("user")


@router.get(
    "",
    response_model=list[PreferedIngredientsResponse],
    dependencies=[Depends(logged_only)],
)
async def get_all_relations_prefered_ingredients(
    requesting_user: User = Depends(validate_token),
):
    return await crud.get_relationships(
        requesting_user.id, "ingredients", find_name=True
    )


@router.post(
    "",
    response_model=PreferedIngredientsCreateResponse,
    dependencies=[Depends(logged_only)],
)
async def create_relation_prefered_ingredients(
    prefered_ingredient: PreferedIngredientsCreate,
    requesting_user: User = Depends(validate_token),
):
    return await crud.post_relationship(
        requesting_user.id, "ingredients", prefered_ingredient
    )


@router.get(
    "/",
    response_model=PreferedIngredientsResponse,
    dependencies=[Depends(logged_only)],
)
async def get_relation_prefered_ingredients(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.get_relationship(
        requesting_user.id, "ingredients", ingredient_id, find_name=True
    )


@router.delete(
    "/",
    response_model=PreferedIngredientsDelete,
    dependencies=[Depends(logged_only)],
)
async def delete_relation_prefered_ingredients(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.delete_relationship(
        requesting_user.id, "ingredients", ingredient_id
    )
