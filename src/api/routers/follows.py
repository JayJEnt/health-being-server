"""/follows router"""
from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.follows import CreateFollows
from api.schemas.user import User


router = APIRouter(prefix="/follows", tags=["follows"])
crud = CrudOperations("user")


"""/follows endpoint"""
@router.get("", dependencies=[Depends(logged_only)])
async def get_all_relations_follows(requesting_user: User = Depends(validate_token)):
    return await crud.get_relationships("user", requesting_user.id)


@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_follows(followed_user: CreateFollows, requesting_user: User = Depends(validate_token)):
    return await crud.post_relationship(requesting_user.id, "user", followed_user)


"""/follows/{followed_user_id} endpoint"""
@router.get("/{followed_user_id}", dependencies=[Depends(logged_only)])
async def get_relation_follows(followed_user_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.get_relationship(requesting_user.id, "user", followed_user_id)


@router.delete("/{followed_user_id}", dependencies=[Depends(logged_only)])
async def delete_relation_follows(followed_user_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.delete_relationship(requesting_user.id, "user", followed_user_id)

