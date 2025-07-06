from fastapi import HTTPException
from botocore.exceptions import ClientError
import boto3
import json
import os
from pathlib import Path

from api.schemas.ingredient import Ingredient
from config import settings


def get_refrigerator_method():
    if settings.environment == "remote":
        s3 = boto3.client("s3")
        bucket_name = os.environ["BUCKET_NAME"]
        file_name = os.environ["REFRIGERATOR_FILE"]
        try:
            response = s3.get_object(Bucket=bucket_name, Key=file_name)
            file_content = response['Body'].read().decode('utf-8')
            return json.loads(file_content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=404, detail=f"File {file_name} not found in bucket.")
            raise HTTPException(status_code=500, detail=str(e))
    else:
        recipes_file = Path("local_data_for_testing/database_refrigerator.json")
        try:
            with open(recipes_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")

def save_refrigerator_method(recipes):
    if settings.environment == "remote":
        s3 = boto3.client("s3")
        bucket_name = os.environ["BUCKET_NAME"]
        file_name = os.environ["REFRIGERATOR_FILE"]
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
        recipes_file = Path("local_data_for_testing/database_refrigerator.json")
        try:
            with open(recipes_file, "w") as file:
                json.dump(recipes, file, indent=2)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")
        
def get_ingredients_method():
    try:
        ingredients = get_refrigerator_method()
        return ingredients
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
def add_ingredient_method(ingredient: Ingredient):
    try:
        new_ingredient = ingredient.dict()
        ingredients = get_refrigerator_method()
        new_ingredient["id"] = len(ingredients) + 1
        ingredients.append(new_ingredient)
        save_refrigerator_method(ingredients)
        return new_ingredient
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_ingredient_method(ingredient_id: int):
    try:
        ingredients = get_refrigerator_method()
        index = next((i for i, r in enumerate(ingredients) if r["id"] == ingredient_id), None)
        if index is None:
            raise HTTPException(status_code=404, detail="Ingredient not found")
            
        deleted_ingredient = ingredients.pop(index)
        save_refrigerator_method(ingredients)
        
        return deleted_ingredient
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ingredients file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))