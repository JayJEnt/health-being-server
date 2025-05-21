from fastapi import HTTPException
from botocore.exceptions import ClientError
import boto3
import json
import os
from pathlib import Path
from typing import Optional, List

from api.schemas.recipe import Recipe
from config import settings

def get_recipes():
    if settings.environment == "remote":
        s3 = boto3.client("s3")
        bucket_name = os.environ["BUCKET_NAME"]
        file_name = os.environ["RECIPES_FILE"]
        try:
            response = s3.get_object(Bucket=bucket_name, Key=file_name)
            file_content = response['Body'].read().decode('utf-8')
            return json.loads(file_content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=404, detail=f"File {file_name} not found in bucket.")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        recipes_file = Path("tests/database_recipes.json")
        try:
            with open(recipes_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")

def save_recipes(recipes):
    if settings.environment == "remote":
        s3 = boto3.client("s3")
        bucket_name = os.environ["BUCKET_NAME"]
        file_name = os.environ["RECIPES_FILE"]
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=recipes,
                ContentType='application/json'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=404, detail=f"File {file_name} not found in bucket.")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        recipes_file = Path("tests/database_recipes.json")
        try:
            with open(recipes_file, "w") as file:
                json.dump(recipes, file, indent=2)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")

def get_recipe(recipe_id: int):
    try:
        recipes = get_recipes()
        recipe = next((r for r in recipes if r["id"] == recipe_id), None)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_recipe(recipe: Recipe):
    try:
        new_recipe = recipe.dict()
        recipes = get_recipes()
        new_recipe["id"] = len(recipes) + 1
        recipes.append(new_recipe)
        save_recipes(recipes)
        return new_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_recipe(recipe_id: int, recipe: Recipe):
    try:
        recipes = get_recipes()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        updated_recipe = recipe.dict()
        updated_recipe["id"] = recipe_id
        recipes[index] = updated_recipe
        
        save_recipes(recipes)
        
        return updated_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_recipe(recipe_id: int):
    try:
        recipes = get_recipes()
        
        index = next((i for i, r in enumerate(recipes) if r["id"] == recipe_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        deleted = recipes.pop(index)
        save_recipes(recipes)
        
        return {"message": "Recipe deleted", "recipe": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def filter_recipes(
    name: Optional[str],
    diet_type: Optional[List[str]],
    ingredient: Optional[List[str]],
    ):
    try:
        recipes = get_recipes()
        
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