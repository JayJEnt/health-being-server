from api.schemas.utils import Quantity


class RefrigeratorCreate(Quantity):
    name: str


class RefrigeratorCreateResponse(RefrigeratorCreate):
    id: int


class RefrigeratorResponse(RefrigeratorCreate):
    ingredient_id: int


class RefrigeratorDelete(Quantity):
    user_id: int
    ingredient_id: int
