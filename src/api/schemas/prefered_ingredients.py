from pydantic import BaseModel


"""Prefered ingredients models"""
class CreatePreferedIngredients(BaseModel):
    name: str
    preference: str

