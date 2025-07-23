from pydantic import BaseModel
from typing import List

from api.schemas.not_used.ingredient import Ingredient


class Refrigerator(BaseModel):
    id: int
    ingredients: List[Ingredient]