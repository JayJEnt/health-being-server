from pydantic import BaseModel
from typing import List, Optional
from api.schemas.ingredient import Ingredient


class Refrigerator(BaseModel):
    id: int
    ingredients: Optional[List[Ingredient]]