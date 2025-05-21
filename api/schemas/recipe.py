from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import Ingredient


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    diet_type: Optional[List[str]]
    ingredients: List[Ingredient]