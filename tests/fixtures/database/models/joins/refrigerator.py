from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from tests.fixtures.database.supabase_connection import Base
from config import settings


class Refrigerator(Base):
    __tablename__ = settings.REFRIGERATOR_TABLE

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    measure_unit = Column(String, nullable=False)

    user = relationship("User", back_populates="refrigerator")
    ingredient = relationship("Ingredient", back_populates="refrigerator")
