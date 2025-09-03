from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class PreferedIngredients(Base):
    __tablename__ = settings.PREFERED_INGREDIENTS_TABLE

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    preference = Column(String, nullable=True)

    user = relationship("User", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="users")
