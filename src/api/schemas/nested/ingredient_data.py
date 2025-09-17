from pydantic import BaseModel
from typing import Optional


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
