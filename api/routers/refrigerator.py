from fastapi import APIRouter

from api.schemas.ingredient import Ingredient
from api.routers.router_methods.refrigerator import (
    get_ingredients_method,
    add_ingredient_method,
    delete_ingredient_method,
)


router = APIRouter()


@router.get("/refrigerator/", response_model=list[Ingredient])
async def get_ingredients():
    return get_ingredients_method()
    
@router.post("/refrigerator/", response_model=Ingredient)
async def add_ingredient(ingredient: Ingredient):
    return add_ingredient_method(ingredient)
    
@router.delete("/refrigerator/{ingredient_id}", response_model=Ingredient)
async def delete_ingredient(ingredient_id: int):
    return delete_ingredient_method(ingredient_id)