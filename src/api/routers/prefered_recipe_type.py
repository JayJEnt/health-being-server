"""/prefered_recipe_type router"""
from fastapi import APIRouter, Depends

from api.schemas.user import User
from api.crud.relation.post_methods import create_relationship
from api.crud.relation.delete_methods import delete_relationship
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/prefered_recipe_type/{diet_type_id}", tags=["prefered_recipe_type"])


"""/prefered_recipe_type/{diet_type_id} endpoint"""
@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_prefered_recipe_type(diet_type_id: int, requesting_user: User = Depends(validate_token)):
    return await create_relationship("diet_type", diet_type_id, "user", requesting_user)


@router.delete("", dependencies=[Depends(logged_only)])
async def delete_relation_prefered_recipe_type(diet_type_id: int, requesting_user: User = Depends(validate_token)):
    return await delete_relationship("diet_type", diet_type_id, "user", requesting_user.id)
