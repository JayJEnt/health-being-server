from pydantic import BaseModel

from api.schemas.enum_utils import Preference


class PreferedIngredientsCreate(BaseModel):
    name: str
    preference: Preference


class PreferedIngredientsCreateResponse(PreferedIngredientsCreate):
    id: int


class PreferedIngredientsResponse(PreferedIngredientsCreate):
    ingredient_id: int


class PreferedIngredientsDelete(BaseModel):
    user_id: int
    ingredient_id: int
    preference: Preference
