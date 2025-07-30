from pydantic import BaseModel
from typing import List, Optional

from src.api.schemas.ingredient import IngredientQuantity
from src.api.schemas.diet_type import DietTypeCreate

class RecipeBaseModel(BaseModel):
    title: str
    image_url: Optional[str] = None
    description: str
    instructions: List[str]

class RecipePage(RecipeBaseModel):
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]

class RecipeOverview(BaseModel):
    id: int
    title: str
    image_url: Optional[str] = None

class Recipe(RecipeOverview):
    description: str
    instructions: List[str]

class RecipePageResponse(Recipe):
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]
