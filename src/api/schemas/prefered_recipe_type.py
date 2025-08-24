from pydantic import BaseModel


"""Prefered recipe type models"""
class CreatePreferedRecipeType(BaseModel):
    name: str
