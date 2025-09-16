"""/refrigerator router"""

from fastapi import APIRouter, Depends

from api.schemas.user import User
from api.crud.crud_operations import CrudOperations
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.schemas.refrigerator import CreateRefrigerator


router = APIRouter(prefix="/refrigerator", tags=["refrigerator"])
crud = CrudOperations("user")


"""/refrigerator endpoint"""


@router.get("", dependencies=[Depends(logged_only)])
async def get_all_relations_refrigerator(
    requesting_user: User = Depends(validate_token),
):
    return await crud.get_relationships(
        requesting_user.id, "refrigerator", find_name=True
    )


@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_refrigerator(
    ingredient: CreateRefrigerator, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "refrigerator", ingredient)


"""/refrigerator/{ingredient_id} endpoint"""


@router.get("/{ingredient_id}", dependencies=[Depends(logged_only)])
async def get_relation_refrigerator(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    return await crud.get_relationship(
        requesting_user.id, "refrigerator", ingredient_id, find_name=True
    )


@router.delete("/{ingredient_id}", dependencies=[Depends(logged_only)])
async def delete_relation_refrigerator(
    ingredient_id: int, requesting_user: User = Depends(validate_token)
):
    return await crud.delete_relationship(
        requesting_user.id, "refrigerator", ingredient_id
    )
