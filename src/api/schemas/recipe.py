from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import IngredientQuantity
from api.schemas.diet_type import DietTypeCreate


"""Recipe models"""
class RecipeCreate(BaseModel):
    title: str
    description: str
    instructions: List[str]
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]

class RecipeOverview(BaseModel):
    id: int
    title: str

class RecipeResponse(RecipeOverview):
    owner_id: int
    description: str
    instructions: List[str]
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]
