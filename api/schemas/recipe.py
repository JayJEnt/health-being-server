from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import Ingredient


class CreateRecipe(BaseModel):
    title: str
    image_url: Optional[str] = None
    description: str
    instructions: List[str]
    diet_type: Optional[List[str]]
    ingredients: List[Ingredient]

class RecipeOverview(BaseModel):
    id: int
    title: str
    image_url: Optional[str] = None

class Recipe(RecipeOverview):
    description: str
    instructions: List[str]
    diet_type: Optional[List[str]]
    ingredients: List[Ingredient]