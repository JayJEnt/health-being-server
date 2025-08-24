"""/recipes router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.recipe import RecipeCreate, RecipeOverview, RecipeResponse
from api.schemas.user import User
from api.crud.single_entity.get_methods import get_elements
from api.crud.many_entites.get_methods import get_all
from api.crud.many_entites.post_methods import create_all
from api.crud.many_entites.delete_methods import delete_all
from api.crud.many_entites.put_methods import update_all
from api.crud.single_entity.search_methods import search_elements
from api.crud.utils import add_attributes
from api.authentication.allowed_roles import logged_only, owner_only
from api.authentication.token import validate_token


router = APIRouter(prefix="/recipes", tags=["recipes"])


"""/recipes endpoint"""
@router.get("", response_model=List[RecipeOverview])
async def get_recipes():
    return await get_elements("recipes", True)

@router.post("", response_model=RecipeResponse, dependencies=[Depends(logged_only)])
async def create_recipe(recipe: RecipeCreate, requesting_user: User = Depends(validate_token)):
    recipe = add_attributes(recipe, [{"owner_id": requesting_user.id}])
    return await create_all("recipes", recipe)




"""/recipes/{recipe_id} endpoint"""
@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int):
    return await get_all("recipes", recipe_id, related_attributes=["ingredients", "diet_type"])

@router.put("/{recipe_id}", response_model=RecipeResponse, dependencies=[Depends(logged_only)])
async def update_recipe(recipe_id: int, recipe: RecipeCreate, requesting_user: User = Depends(validate_token)):
    owner_only("recipes", recipe_id, requesting_user)

    return await update_all("recipes", recipe_id, recipe)

@router.delete("/{recipe_id}", dependencies=[Depends(logged_only)])
async def delete_recipe(recipe_id: int, requesting_user: User = Depends(validate_token)):
    owner_only("recipes", recipe_id, requesting_user)

    return await delete_all("recipes", recipe_id)




"""/recipes/search/{phrase} endpoint"""
@router.get("/search/{phrase}", response_model=List[RecipeOverview])
async def search_recipes(phrase: str):
    return await search_elements("recipes", phrase, True)




admin_router = APIRouter(prefix="/admin/recipes", tags=["admin: recipes"])


# TODO: Add admin routers