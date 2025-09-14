from pydantic import BaseModel

from api.schemas.enum_utils import MeasureUnit


class CreateRefrigerator(BaseModel):
    name: str
    amount: float
    measure_unit: MeasureUnit


class PostCreateRefrigerator(CreateRefrigerator):
    id: int


class Refrigerator(BaseModel):
    user_id: int
    ingredient_id: int
    amount: float
    measure_unit: MeasureUnit


class RefrigeratorGet(BaseModel):
    users: str
    ingredients: str
    amount: float
    measure_unit: MeasureUnit
