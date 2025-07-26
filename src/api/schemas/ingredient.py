from pydantic import BaseModel
from typing import List, Optional

from api.schemas.vitamin import Vitamin


class CreateIngredient(BaseModel):
    name: str

    # Optional fields
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0

    vitamins: Optional[List[Vitamin]] = None
    
class Ingredient(CreateIngredient):
    id: int

class IngredientQuantity(Ingredient):
    amount: float  # ex. 100g, 1l, 2szt.
    measure_unit: str  # ex. "g", "ml", "szt."