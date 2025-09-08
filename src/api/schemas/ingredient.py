from pydantic import BaseModel
from typing import List, Optional

from api.schemas.vitamin import VitaminCreate, Vitamin


"""Ingredient base models"""


class IngredientName(BaseModel):
    name: str


class IngredientIndex(BaseModel):
    id: int


"""Ingredient data models"""


class IngredientDataCreate(BaseModel):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0


class IngredientDataResponse(IngredientDataCreate):
    ingredient_id: int


"""Ingredient models"""


class Ingredient(IngredientName, IngredientIndex):
    pass


class IngredientCreate(IngredientName):
    vitamins: Optional[List[VitaminCreate]] = None
    ingredients_data: Optional[IngredientDataCreate]


class IngredientResponse(Ingredient):
    vitamins: Optional[List[Vitamin]] = None
    ingredients_data: Optional[IngredientDataResponse] = None


class IngredientUpdate(IngredientName):
    vitamins: Optional[List[VitaminCreate]] = None


class IngredientUpdateResponse(Ingredient):
    vitamins: Optional[List[Vitamin]] = None


"""Ingredient included models"""


class IngredientQuantity(IngredientName):
    amount: float  # ex. 100g, 1l, 2szt.
    measure_unit: str  # ex. "g", "ml", "szt."
