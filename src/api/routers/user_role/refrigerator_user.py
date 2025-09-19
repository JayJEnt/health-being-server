"""/refrigerator router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.refrigerator import (
    RefrigeratorCreate,
    RefrigeratorCreateResponse,
    RefrigeratorResponse,
    RefrigeratorDelete,
)
from api.schemas.user import User


router = APIRouter(prefix="/refrigerator", tags=["user: refrigerator"])
crud = CrudOperations("user")


@router.get(
    "", response_model=list[RefrigeratorResponse], dependencies=[Depends(logged_only)]
)
async def get_all_relations_refrigerator(
    requesting_user: User = Depends(validate_token),
):
    return await crud.get_relationships(
        requesting_user.id, "refrigerator", find_name=True
    )


@router.post(
    "", response_model=RefrigeratorCreateResponse, dependencies=[Depends(logged_only)]
)
async def create_relation_refrigerator(
    ingredient: RefrigeratorCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "refrigerator", ingredient)


@router.get(
    "/", response_model=RefrigeratorResponse, dependencies=[Depends(logged_only)]
)
async def get_relation_refrigerator(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.get_relationship(
        requesting_user.id, "refrigerator", ingredient_id, find_name=True
    )


@router.delete(
    "/", response_model=RefrigeratorDelete, dependencies=[Depends(logged_only)]
)
async def delete_relation_refrigerator(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    if not ingredient_id:
        raise DemandQueryParameter
    return await crud.delete_relationship(
        requesting_user.id, "refrigerator", ingredient_id
    )
