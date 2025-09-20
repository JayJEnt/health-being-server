from pydantic import BaseModel
from typing import List, Optional

from api.schemas.enum_utils import MeasureUnit
from api.schemas.vitamin import VitaminCreate, Vitamin


class IngredientName(BaseModel):
    name: str


class IngredientIndex(BaseModel):
    id: int


class IngredientDataCreate(BaseModel):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0


class IngredientData(IngredientDataCreate):
    ingredient_id: int


class Ingredient(IngredientName, IngredientIndex):
    pass


class IngredientCreate(IngredientName):
    vitamins: Optional[List[VitaminCreate]] = None
    ingredients_data: Optional[IngredientDataCreate]


class IngredientResponse(Ingredient, IngredientDataCreate):
    vitamins: Optional[List[Vitamin]] = None


class IngredientUpdate(IngredientName):
    vitamins: Optional[List[VitaminCreate]] = None


class IngredientUpdateResponse(Ingredient):
    vitamins: Optional[List[Vitamin]] = None


class Quantity(BaseModel):
    amount: float
    measure_unit: MeasureUnit


class IngredientQuantity(IngredientName, Quantity):
    pass
