from pydantic import BaseModel

from api.schemas.enum_utils import Preference


"""Prefered ingredients models"""


class CreatePreferedIngredients(BaseModel):
    name: str
    preference: Preference


class PostCreatePreferedIngredients(CreatePreferedIngredients):
    id: int


class PreferedIngredients(BaseModel):
    user_id: int
    ingredient_id: int
    preference: Preference


class PreferedIngredientsGet(BaseModel):
    users: str
    ingredients: str
    preference: Preference
