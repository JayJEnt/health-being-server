from pydantic import BaseModel
from typing import List

from api.schemas.ingredient import IngredientQuantity


class Refrigerator(BaseModel):
    user_id: int
    ingredients: List[IngredientQuantity]