from sqlmodel import Field, SQLModel

from typing import List, Optional

from api.schemas.enum_utils import MeasureUnit
from api.schemas.nested.ingredient_data import IngredientDataCreate
from api.schemas.vitamin import VitaminCreate, VitaminResponse


class IngredientBase(SQLModel):
    name: str = Field(unique=True, nullable=False)


class IngredientCreate(IngredientBase):
    pass


class IngredientDB(IngredientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class IngredientResponse(IngredientBase):
    id: int


class IngredientCreateAll(IngredientBase):
    vitamins: Optional[List[VitaminCreate]] = None
    ingredients_data: Optional[IngredientDataCreate]


class IngredientResponse(IngredientResponse, IngredientDataCreate):
    vitamins: Optional[List[VitaminResponse]] = None


class IngredientUpdate(IngredientBase):
    vitamins: Optional[List[VitaminCreate]] = None


class IngredientUpdateResponse(IngredientResponse):
    vitamins: Optional[List[VitaminResponse]] = None


"""Ingredient included models"""


class IngredientQuantity(IngredientBase):
    amount: float
    measure_unit: MeasureUnit
