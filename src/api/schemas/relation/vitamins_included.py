from sqlmodel import Field, SQLModel

from api.schemas.enum_utils import MeasureUnit

# from api.schemas.ingredient import IngredientDB
# from api.schemas.vitamin import VitaminDB


class VitaminsIncludedBase(SQLModel):
    amount: float = Field(nullable=False)
    measure_unit: MeasureUnit = Field(nullable=False)


# class VitaminsIncludedDB(VitaminsIncludedBase, table=True):
#     __tablename__ = settings.VITAMINS_INCLUDED_TABLE

#     vitamin_id: int = Field(foreign_key=f"{settings.VITAMIN_TABLE}.id", primary_key=True)
#     ingredient_id: int = Field(foreign_key=f"{settings.INGREDIENT_TABLE}.id", primary_key=True)

#     vitamin: VitaminDB = Relationship(back_populates="ingredients")
#     ingredient: IngredientDB = Relationship(back_populates="vitamins")
