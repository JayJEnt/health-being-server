"""/recipes router"""
from fastapi import APIRouter, Depends

from typing import List

from api.schemas.recipe import RecipePage, RecipeOverview, RecipePageResponse
from api.crud.get_methods import get_elements, get_element_by_id
from api.crud.post_methods import create_element
from api.crud.delete_methods import delete_element_by_id
from api.crud.put_methods import update_element_by_id
from api.crud.search_methods import search_elements
from api.authentication.allowed_roles import logged_only


router = APIRouter(prefix="/recipes", tags=["recipes"])


"""/recipes endpoint"""
@router.get("", response_model=List[RecipeOverview])
async def get_recipes():
    return await get_elements("recipes", True)

@router.post("", response_model=RecipePageResponse, dependencies=[Depends(logged_only)])
async def create_recipe(recipe: RecipePage):
    return await create_element("recipes", recipe)




"""/recipes/{recipe_id} endpoint"""
@router.get("/{recipe_id}", response_model=RecipePageResponse)
async def get_recipe(recipe_id: int):
    return await get_element_by_id("recipes", recipe_id)

@router.put("/{recipe_id}", response_model=RecipePageResponse)
async def update_recipe(recipe_id: int, recipe: RecipePage):
    return await update_element_by_id("recipes", recipe_id, recipe)

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int):
    return await delete_element_by_id("recipes", recipe_id)




"""/recipes/search/{phrase} endpoint"""
@router.get("/search/{phrase}", response_model=List[RecipeOverview])
async def search_recipes(phrase: str):
    return await search_elements("recipes", phrase, True)
