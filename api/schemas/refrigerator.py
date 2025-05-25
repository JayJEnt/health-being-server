from pydantic import BaseModel
from typing import List

from api.schemas.ingredient import Ingredient


class Refrigerator(BaseModel):
    id: int
    ingredients: List[Ingredient]