from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from tests.fixtures.database.supabase_connection import Base
from config import settings


class VitaminsIncluded(Base):
    __tablename__ = settings.VITAMINS_INCLUDED_TABLE

    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    vitamin_id = Column(Integer, ForeignKey("vitamins.id"), primary_key=True)

    ingredient = relationship("Ingredient", back_populates="vitamins")
    vitamin = relationship("Vitamin", back_populates="ingredients")
