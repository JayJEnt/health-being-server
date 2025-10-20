from pydantic import BaseModel

from typing import Optional

from api.schemas.enum_utils import MeasureUnit


class Quantity(BaseModel):
    amount: float
    measure_unit: MeasureUnit


class Micronutrients(BaseModel):
    calories_per_100: Optional[float] = 0.0
    protein_per_100: Optional[float] = 0.0
    fat_per_100: Optional[float] = 0.0
    carbon_per_100: Optional[float] = 0.0
    fiber_per_100: Optional[float] = 0.0
    sugar_per_100: Optional[float] = 0.0
    salt_per_100: Optional[float] = 0.0


class MicronutrientsTotal(BaseModel):
    calories: float = 0.0
    protein: float = 0.0
    fat: float = 0.0
    carbon: float = 0.0
    fiber: float = 0.0
    sugar: float = 0.0
    salt: float = 0.0
