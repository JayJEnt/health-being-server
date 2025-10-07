from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from tests.fixtures.database.supabase_connection import Base
from config import settings


class Ingredient(Base):
    __tablename__ = settings.INGREDIENT_TABLE

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    calories_per_100 = Column(Float, default=0.0)
    protein_per_100 = Column(Float, default=0.0)
    fat_per_100 = Column(Float, default=0.0)
    carbon_per_100 = Column(Float, default=0.0)
    fiber_per_100 = Column(Float, default=0.0)
    sugar_per_100 = Column(Float, default=0.0)
    salt_per_100 = Column(Float, default=0.0)

    # N:M
    vitamins = relationship("VitaminsIncluded", back_populates="ingredient")
    users = relationship("PreferedIngredients", back_populates="ingredient")
    refrigerator = relationship("Refrigerator", back_populates="ingredient")
    recipes = relationship("IngredientsIncluded", back_populates="ingredient")
