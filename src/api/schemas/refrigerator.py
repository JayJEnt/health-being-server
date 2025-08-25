from pydantic import BaseModel
from typing import List

from api.schemas.ingredient import IngredientQuantity

# NOT IN USE TODO: maybe delete?
class Refrigerator(BaseModel):
    user_id: int
    ingredients: List[IngredientQuantity]

class AddToRefrigerator(BaseModel):
    name: str
    amount: str