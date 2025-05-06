from pydantic import BaseModel
from typing import List, Optional
from api.schemas.ingredient import Ingredient
from api.schemas.dietary_type import DietaryType


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    diet_type: Optional[List[DietaryType]]
    ingredients: List[Ingredient]