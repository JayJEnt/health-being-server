from fastapi import APIRouter, HTTPException
from api.schemas.ingredient import Ingredient
import json
from pathlib import Path


router = APIRouter()
REGRIGERATOR_FILE = Path("database_refrigerator.json")

def get_refrigerator_content_from_file():
    with open(REGRIGERATOR_FILE, "r") as file:
        return json.load(file)

def save_refrigerator_content_to_file(recipes):
    with open(REGRIGERATOR_FILE, "w") as file:
        json.dump(recipes, file, indent=2)


@router.get("/refrigerator/", response_model=list[Ingredient])
async def get_ingredients():
    try:
        ingredients = get_refrigerator_content_from_file()
        return ingredients
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/refrigerator/", response_model=Ingredient)
async def add_ingredient(ingredient: Ingredient):
    try:
        new_ingredient = ingredient.dict()
        ingredients = get_refrigerator_content_from_file()
        new_ingredient["id"] = len(ingredients) + 1
        ingredients.append(new_ingredient)
        save_refrigerator_content_to_file(ingredients)
        return new_ingredient
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/refrigerator/{ingredient_id}", response_model=Ingredient)
async def delete_ingredient(ingredient_id: int):
    try:
        ingredients = get_refrigerator_content_from_file()
        index = next((i for i, r in enumerate(ingredients) if r["id"] == ingredient_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Ingredient not found")
            
        deleted_ingredient = ingredients.pop(index)
        save_refrigerator_content_to_file(ingredients)
        
        return deleted_ingredient
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))