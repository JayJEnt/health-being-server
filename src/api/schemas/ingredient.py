from pydantic import BaseModel
from typing import List, Optional

from api.schemas.utils import Quantity
from api.schemas.vitamin import VitaminCreate, Vitamin


class IngredientName(BaseModel):
    name: str


class Ingredient(IngredientName):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0


class IngredientResponse(Ingredient):
    id: int


class IngredientCreate(Ingredient):
    vitamins: Optional[List[VitaminCreate]] = None


class IngredientResponseAll(IngredientResponse):
    vitamins: Optional[List[Vitamin]] = None


class IngredientQuantity(IngredientName, Quantity):
    pass
