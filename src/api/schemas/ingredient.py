from pydantic import BaseModel
from typing import List, Optional

from api.schemas.vitamin import CreateVitamin


class CreateIngredient(BaseModel):
    name: str

class CreateIngredientQuantity(CreateIngredient):
    amount: float  # ex. 100g, 1l, 2szt.
    measure_unit: str  # ex. "g", "ml", "szt."

# Detailed below

class CreateDetailedIngredient(CreateIngredient):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0

    vitamins: Optional[List[CreateVitamin]] = None
    
class Ingredient(CreateDetailedIngredient):
    id: int

class IngredientQuantity(Ingredient):
    amount: float  # ex. 100g, 1l, 2szt.
    measure_unit: str  # ex. "g", "ml", "szt."