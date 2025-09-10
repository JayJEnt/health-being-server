from pydantic import BaseModel


"""Prefered ingredients models"""


class CreatePreferedIngredients(BaseModel):
    name: str
    preference: str


class PostCreatePreferedIngredients(CreatePreferedIngredients):
    id: int


class PreferedIngredients(BaseModel):
    user_id: int
    ingredient_id: int
    preference: str
