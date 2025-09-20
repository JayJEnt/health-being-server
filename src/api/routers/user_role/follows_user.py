"""/follows router"""

from fastapi import APIRouter, Depends

from typing import List, Union

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.follows import FollowsCreate, Follows, FollowsDelete
from api.schemas.user import User


router = APIRouter(prefix="/follows", tags=["user: follows"])
crud = CrudOperations("user")


@router.get(
    "",
    response_model=Union[Follows, List[Follows]],
    dependencies=[Depends(logged_only)],
)
async def get_relation_follows(
    followed_user_id: int = None, requesting_user: User = Depends(validate_token)
):
    if followed_user_id:
        return await crud.get_relationship(
            requesting_user.id, "user", followed_user_id, find_name=True
        )
    return await crud.get_relationships(requesting_user.id, "user", find_name=True)


@router.post("", response_model=User, dependencies=[Depends(logged_only)])
async def create_relation_follows(
    followed_user: FollowsCreate, requesting_user: User = Depends(validate_token)
):
    return await crud.post_relationship(requesting_user.id, "user", followed_user)


@router.delete("", response_model=FollowsDelete, dependencies=[Depends(logged_only)])
async def delete_relation_follows(
    followed_user_id: int, requesting_user: User = Depends(validate_token)
):
    return await crud.delete_relationship(requesting_user.id, "user", followed_user_id)
