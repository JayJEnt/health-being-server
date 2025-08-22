"""/prefered_ingredients router"""
from fastapi import APIRouter, Depends

from api.schemas.user import User
from api.crud.relations_nm.post_methods import create_relationship
from api.crud.relations_nm.delete_methods import delete_relationship
from api.crud.utils import add_attributes
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/prefered_ingredients/{ingredient_id}", tags=["prefered_ingredients"])


"""/prefered_ingredients/{ingredient_id} endpoint"""
@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_prefered_ingredients(ingredient_id: int, preference: str, requesting_user: User = Depends(validate_token)):
    requesting_user = add_attributes(requesting_user, [{"preference": preference}])
    return await create_relationship("ingredients", ingredient_id, "user", requesting_user)


@router.delete("", dependencies=[Depends(logged_only)])
async def delete_relation_prefered_ingredients(ingredient_id: int, requesting_user: User = Depends(validate_token)):
    return await delete_relationship("ingredients", ingredient_id, "user", requesting_user.id)
