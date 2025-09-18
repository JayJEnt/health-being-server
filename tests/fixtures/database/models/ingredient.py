from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from tests.fixtures.database.supabase_connection import Base
from config import settings


class Ingredient(Base):
    __tablename__ = settings.INGREDIENT_TABLE

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # 1:1
    ingredient_data = relationship(
        "IngredientData", back_populates="ingredient", uselist=False
    )

    # N:M
    vitamins = relationship("VitaminsIncluded", back_populates="ingredient")
    users = relationship("PreferedIngredients", back_populates="ingredient")
    refrigerator = relationship("Refrigerator", back_populates="ingredient")
    recipes = relationship("IngredientsIncluded", back_populates="ingredient")
