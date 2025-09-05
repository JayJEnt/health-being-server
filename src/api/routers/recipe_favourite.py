"""/recipe_favourite router"""
from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.crud.crud_operations import CrudOperations
from api.schemas.recipe_favourite import CreateRecipeFavourite
from api.schemas.user import User


router = APIRouter(prefix="/recipe_favourite", tags=["recipe_favourite"])
crud = CrudOperations("user")


"""/recipe_favourite endpoint"""
@router.get("", dependencies=[Depends(logged_only)])
async def get_all_relations_recipe_favourite(requesting_user: User = Depends(validate_token)):
    return await crud.get_relationships(requesting_user.id, "recipes")


@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_recipe_favourite(recipe: CreateRecipeFavourite, requesting_user: User = Depends(validate_token)):
    return await crud.post_relationship(requesting_user.id, "recipes", recipe)


"""/recipe_favourite/{recipe_id} endpoint"""
@router.get("/{recipe_id}", dependencies=[Depends(logged_only)])
async def get_relation_recipe_favourite(recipe_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.get_relationship(requesting_user.id, "recipes", recipe_id)


@router.delete("/{recipe_id}", dependencies=[Depends(logged_only)])
async def delete_relation_recipe_favourite(recipe_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.delete_relationship(requesting_user.id, "recipes", recipe_id)

