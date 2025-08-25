"""/prefered_recipe_type router"""
from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.prefered_recipe_type import CreatePreferedRecipeType
from api.schemas.user import User


router = APIRouter(prefix="/prefered_recipe_type", tags=["prefered_recipe_type"])
crud = CrudOperations("user")


"""/prefered_recipe_type endpoint"""
@router.get("", dependencies=[Depends(logged_only)])
async def get_all_relations_prefered_recipe_type(requesting_user: User = Depends(validate_token)):
    return await crud.get_relationships("diet_type", requesting_user.id)


@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_prefered_recipe_type(diet_type: CreatePreferedRecipeType, requesting_user: User = Depends(validate_token)):
    return await crud.post_relationship(requesting_user.id, "diet_type", diet_type)


"""/prefered_recipe_type/{diet_type_id} endpoint"""
@router.get("/{diet_type_id}", dependencies=[Depends(logged_only)])
async def get_relation_prefered_recipe_type(diet_type_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.get_relationship(requesting_user.id, "diet_type", diet_type_id)


@router.delete("/{diet_type_id}", dependencies=[Depends(logged_only)])
async def delete_relation_prefered_recipe_type(diet_type_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.delete_relationship(requesting_user.id, "diet_type", diet_type_id)

