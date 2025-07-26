from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import CreateIngredientQuantity, IngredientQuantity
from api.schemas.diet_type import CreateDietType, DietType


class CreateRecipe(BaseModel):
    title: str
    image_url: Optional[str] = None
    description: str
    instructions: str

class CreateDetailedRecipe(CreateRecipe):
    diet_type: Optional[List[CreateDietType]] = None
    ingredients: List[CreateIngredientQuantity]

class RecipeOverview(BaseModel):
    id: int
    title: str
    image_url: Optional[str] = None

class Recipe(RecipeOverview):
    description: str
    instructions: str

class DetailedRecipe(Recipe):
    diet_type: Optional[List[DietType]] = None
    ingredients: List[IngredientQuantity]