from fastapi import APIRouter, Query
from typing import Optional, List

from api.schemas.recipe import Recipe
from api.router_methods.recipes import (
    get_recipes_method,
    get_recipe_method,
    create_recipe_method,
    update_recipe_method,
    delete_recipe_method,
    filter_recipes_method
)


router = APIRouter()


@router.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    return get_recipes_method()

@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    return get_recipe_method(recipe_id)

@router.post("/recipes/", response_model=Recipe)
async def create_recipe(recipe: Recipe):
    return create_recipe_method(recipe)

@router.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe: Recipe):
    return update_recipe_method(recipe_id, recipe)

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    return delete_recipe_method(recipe_id)
    
@router.get("/recipes/filter/", response_model=List[Recipe])
async def filter_recipes(
    name: Optional[str] = Query(None, description="Fragment nazwy przepisu"),
    diet_type: Optional[List[str]] = Query(None, description="Lista typów diet"),
    ingredient: Optional[List[str]] = Query(None, description="Lista wymaganych składników")
    ):
    return filter_recipes_method(
        name=name,
        diet_type=diet_type,
        ingredient=ingredient
    )