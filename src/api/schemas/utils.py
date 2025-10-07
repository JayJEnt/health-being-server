from pydantic import BaseModel

from api.schemas.enum_utils import MeasureUnit


class Quantity(BaseModel):
    amount: float
    measure_unit: MeasureUnit
