from pydantic import BaseModel
from typing import List, Optional

from api.schemas.ingredient import IngredientQuantity
from api.schemas.diet_type import DietTypeCreate
from api.schemas.utils import MicronutrientsTotal


class RecipeCreate(BaseModel):
    title: str
    description: str
    instructions: List[str]
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]
    category: str


class RecipeOverview(BaseModel):
    id: int
    title: str


class Recipe(RecipeOverview):
    owner_id: int
    description: str
    instructions: List[str]
    category: str


class RecipeResponse(Recipe):
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]


class RecipeResponseGet(Recipe):
    diet_type: Optional[List[DietTypeCreate]] = None
    ingredients: List[IngredientQuantity]
    micronutrients: Optional[MicronutrientsTotal] = None
