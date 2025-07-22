from fastapi import APIRouter, HTTPException

from api.schemas.recipe import RecipeDetailed as Recipe #TODO: change to recipe when database is updated
from api.routers.router_methods.recipes import (
    get_recipes_method,
    save_recipes_method,
)


router = APIRouter()


@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    try:
        recipes = get_recipes_method()
        recipe = next((r for r in recipes if r["id"] == recipe_id), None)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe: Recipe):
    try:
        recipes = get_recipes_method()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        updated_recipe = recipe.dict()
        updated_recipe["id"] = recipe_id
        recipes[index] = updated_recipe
        
        save_recipes_method(recipes)
        
        return updated_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    try:
        recipes = get_recipes_method()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        deleted = recipes.pop(index)
        save_recipes_method(recipes)
        
        return {"message": "Recipe deleted", "recipe": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))