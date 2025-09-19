from pydantic import BaseModel

from api.schemas.enum_utils import MeasureUnit


class RefrigeratorBase(BaseModel):
    amount: float
    measure_unit: MeasureUnit


class RefrigeratorCreate(RefrigeratorBase):
    name: str


class RefrigeratorCreateResponse(RefrigeratorCreate):
    id: int


class RefrigeratorResponse(RefrigeratorCreate):
    ingredient_id: int


class RefrigeratorDelete(RefrigeratorBase):
    user_id: int
    ingredient_id: int
