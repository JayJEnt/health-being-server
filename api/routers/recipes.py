from fastapi import APIRouter, HTTPException

from typing import List

from api.schemas.recipe import RecipeDetailed as Recipe #TODO: change to recipe when database is updated
from api.routers.router_methods.recipes import (
    get_recipes_method,
    save_recipes_method,
)


router = APIRouter()


@router.get("/recipes/", response_model=List[Recipe])
async def get_recipes():
    get_recipes_method()

@router.post("/recipes/", response_model=Recipe)
async def create_recipe(recipe: Recipe):
    try:
        new_recipe = recipe.dict()
        recipes = get_recipes_method()
        new_recipe["id"] = len(recipes) + 1
        recipes.append(new_recipe)
        save_recipes_method(recipes)
        return new_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



"""Legacy code"""

# @router.get("/recipes/filter/", response_model=List[Recipe])
# async def filter_recipes(
#     name: Optional[str] = Query(None, description="Fragment nazwy przepisu"),
#     diet_type: Optional[List[str]] = Query(None, description="Lista typów diet"),
#     ingredient: Optional[List[str]] = Query(None, description="Lista wymaganych składników")
#     ):
#     return filter_recipes_method(
#         name=name,
#         diet_type=diet_type,
#         ingredient=ingredient
#     )

# def filter_recipes_method(
#     name: Optional[str],
#     diet_type: Optional[List[str]],
#     ingredient: Optional[List[str]],
#     ):
#     try:
#         recipes = get_recipes_method()
        
#         filtered = recipes
        
#         if name:
#             filtered = [r for r in filtered if name.lower() in r["name"].lower()]
            
#         if diet_type:
#             filtered = [
#                 r for r in filtered 
#                 if any(dt in r.get("diet_type", []) for dt in diet_type)
#             ]
#         if ingredient:
#             filtered = [
#                 r for r in filtered 
#                 if any(ing["name"].lower() in [i.lower() for i in ingredient] 
#                       for ing in r["ingredients"])
#             ]
            
#         return filtered
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))