from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class IngredientData(Base):
    __tablename__ = settings.INGREDIENT_DATA_TABLE

    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    calories_per_100 = Column(Float, default=0.0)
    protein_per_100 = Column(Float, default=0.0)
    fat_per_100 = Column(Float, default=0.0)
    carbon_per_100 = Column(Float, default=0.0)
    fiber_per_100 = Column(Float, default=0.0)
    sugar_per_100 = Column(Float, default=0.0)
    salt_per_100 = Column(Float, default=0.0)

    ingredient = relationship(
        "Ingredient", back_populates="ingredient_data", uselist=False
    )
