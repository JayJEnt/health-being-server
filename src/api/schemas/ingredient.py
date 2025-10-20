from pydantic import BaseModel
from typing import List, Optional

from api.schemas.utils import Quantity, Micronutrients
from api.schemas.vitamin import VitaminCreate, Vitamin


class IngredientName(BaseModel):
    name: str


class Ingredient(IngredientName, Micronutrients):
    default_weight: Optional[float] = None
    rho: Optional[float] = None


class IngredientResponse(Ingredient):
    id: int


class IngredientCreate(Ingredient):
    vitamins: Optional[List[VitaminCreate]] = None


class IngredientResponseAll(IngredientResponse):
    vitamins: Optional[List[Vitamin]] = None


class IngredientQuantity(IngredientName, Quantity):
    pass
