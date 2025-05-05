from fastapi import FastAPI, HTTPException, Query
from api.schemas.recipe import Recipe
import json
from pathlib import Path
from typing import Optional, List


router = FastAPI()
RECIPES_FILE = Path("database_recipes.json")

def get_recipes_from_file():
    with open(RECIPES_FILE, "r") as file:
        return json.load(file)

def save_recipes_to_file(recipes):
    with open(RECIPES_FILE, "w") as file:
        json.dump(recipes, file, indent=2)

@router.get("/recipes/", response_model=List[Recipe])
def get_recipes():
    recipes = get_recipes_from_file()
    return recipes

@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    try:
        recipes = get_recipes_from_file()
        recipe = next((r for r in recipes if r["id"] == recipe_id), None)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    try:
        new_recipe = recipe.dict()
        recipes = get_recipes_from_file()
        new_recipe["id"] = len(recipes) + 1
        recipes.append(new_recipe)
        save_recipes_to_file(recipes)
        return new_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe):
    try:
        recipes = get_recipes_from_file()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        updated_recipe = recipe.dict()
        updated_recipe["id"] = recipe_id
        recipes[index] = updated_recipe
        
        save_recipes_to_file(recipes)
        
        return updated_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    try:
        recipes = get_recipes_from_file()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        deleted = recipes.pop(index)
        save_recipes_to_file(recipes)
        
        return {"message": "Recipe deleted", "recipe": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/recipes/filter/", response_model=List[Recipe])
def filter_recipes(
    name: Optional[str] = Query(None, description="Fragment nazwy przepisu"),
    diet_type: Optional[List[str]] = Query(None, description="Lista typów diet"),
    ingredient: Optional[List[str]] = Query(None, description="Lista wymaganych składników")
):
    try:
        recipes = get_recipes_from_file()
        
        filtered = recipes
        
        if name:
            filtered = [r for r in filtered if name.lower() in r["name"].lower()]
            
        if diet_type:
            filtered = [
                r for r in filtered 
                if any(dt in r.get("diet_type", []) for dt in diet_type)
            ]
        if ingredient:
            filtered = [
                r for r in filtered 
                if any(ing["name"].lower() in [i.lower() for i in ingredient] 
                      for ing in r["ingredients"])
            ]
            
        return filtered
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))