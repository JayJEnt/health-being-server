from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import Ingredient


class Recipe(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    
class RecipeDetailed(Recipe):
    description: str
    instructions: str
    diet_type: Optional[List[str]]
    ingredients: List[Ingredient]