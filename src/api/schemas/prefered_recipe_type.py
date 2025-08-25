from pydantic import BaseModel


"""Prefered recipe type models"""
class CreatePreferedRecipeType(BaseModel):
    diet_name: str
