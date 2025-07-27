from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import IngredientQuantity
from api.schemas.diet_type import DietTypeCreate

class RecipeBaseModel(BaseModel):
    title: str
    image_url: Optional[str] = None
    description: str
    instructions: str           # TODO: has to be a dict or list

class RecipePage(RecipeBaseModel):
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]

class RecipeOverview(BaseModel):
    id: int
    title: str
    image_url: Optional[str] = None

class Recipe(RecipeOverview):
    description: str
    instructions: str
