from pydantic import BaseModel
from typing import List, Optional
from api.schemas.vitamin import Vitamin


class IngredientBase(BaseModel):
    id: int
    name: str
    unit: str  # ex. "g", "ml", "szt."
    calories_per_100: float
    protein_per_100: float
    fat_per_100: float
    carbs_per_100: float
    
    # Optional fields
    fiber_per_100: Optional[float]
    sugar_per_100: Optional[float]
    salt_per_100: Optional[float]
    vitamins: Optional[List[Vitamin]] = None
    
class Ingredient(IngredientBase):
    amount: float  # ex. 100g, 1l, 2szt.
