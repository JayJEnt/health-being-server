from pydantic import BaseModel
from typing import List, Optional
from api.schemas.vitamin import Vitamin


class Ingredient(BaseModel):
    id: int
    name: str
    unit: str  # ex. "g", "ml", "szt."
    calories_per_100: float
    protein_per_100: float
    fat_per_100: float
    carbs_per_100: float
    sugar_per_100: float
    salt_per_100: float
    vitamins: Optional[List[Vitamin]] = None
