"""/prefered_ingredients router"""
from fastapi import APIRouter, Depends

from api.crud.crud_operations import CrudOperations
from api.authentication.allowed_roles import logged_only
from api.authentication.token import validate_token
from api.schemas.prefered_ingredients import CreatePreferedIngredients
from api.schemas.user import User


router = APIRouter(prefix="/prefered_ingredients", tags=["prefered_ingredients"])
crud = CrudOperations("user")


"""/prefered_ingredients endpoint"""
@router.get("", dependencies=[Depends(logged_only)])
async def get_all_relations_prefered_ingredients(requesting_user: User = Depends(validate_token)):
    return await crud.get_relationships("ingredients", requesting_user.id)


@router.post("", dependencies=[Depends(logged_only)])
async def create_relation_prefered_ingredients(prefered_ingredient: CreatePreferedIngredients, requesting_user: User = Depends(validate_token)):
    return await crud.post_relationship(requesting_user.id, "ingredients", prefered_ingredient)


"""/prefered_ingredients/{ingredient_id} endpoint"""
@router.get("/{ingredient_id}", dependencies=[Depends(logged_only)])
async def get_relation_prefered_ingredients(ingredient_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.get_relationship(requesting_user.id, "ingredients", ingredient_id)


@router.delete("/{ingredient_id}", dependencies=[Depends(logged_only)])
async def delete_relation_prefered_ingredients(ingredient_id: int, requesting_user: User = Depends(validate_token)):
    return await crud.delete_relationship(requesting_user.id, "ingredients", ingredient_id)
