from pydantic import BaseModel
from typing import List, Optional

from api.schemas.not_used.ingredient import Ingredient


class Recipe(BaseModel):
    id: int
    title: str
    description: str
    type: Optional[str]
    
# class RecipeDetailed(Recipe):
#     image_url: Optional[str] = None
#     instructions: str
#     diet_type: Optional[List[str]]
#     ingredients: List[Ingredient]