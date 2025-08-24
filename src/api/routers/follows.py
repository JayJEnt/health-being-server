"""/follows router"""
from fastapi import APIRouter, Depends

from api.schemas.user import User
from api.crud.relation.post_methods import create_relationship
from api.crud.relation.delete_methods import delete_relationship
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/follows/{followed_user_id}", tags=["follows"])


"""/follows/{followed_user_id} endpoint"""
@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_follows(followed_user_id: int, requesting_user: User = Depends(validate_token)):
    return await create_relationship("user", followed_user_id, "user", requesting_user)


@router.delete("", dependencies=[Depends(logged_only)])
async def delete_relation_follows(followed_user_id: int, requesting_user: User = Depends(validate_token)):
    return await delete_relationship("user", followed_user_id, "user", requesting_user.id)

