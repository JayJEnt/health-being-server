from pydantic import BaseModel
from typing import List, Optional

from api.schemas.vitamin import VitaminCreate, Vitamin


class IngredientBaseModel(BaseModel):
    name: str

class IngredientDetailedModel(IngredientBaseModel):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0

class IngredientCreate(IngredientDetailedModel):
    vitamins: Optional[List[VitaminCreate]] = None
    
class Ingredient(IngredientDetailedModel):
    id: int

class IngredientResponse(Ingredient):
    vitamins: Optional[List[Vitamin]] = None

# Models used by other models/endpoins

class IngredientQuantity(IngredientBaseModel):
    amount: float  # ex. 100g, 1l, 2szt.
    measure_unit: str  # ex. "g", "ml", "szt."
