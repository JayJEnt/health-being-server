from fastapi import HTTPException
from botocore.exceptions import ClientError
import boto3

import os
import json
from pathlib import Path

from config import settings


def get_recipes_method():
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
        recipes_file = Path("local_data_for_testing/database_recipes.json")
        try:
            with open(recipes_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")

def save_recipes_method(recipes):
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
        recipes_file = Path("local_data_for_testing/database_recipes.json")
        try:
            with open(recipes_file, "w") as file:
                json.dump(recipes, file, indent=2)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="File not found")