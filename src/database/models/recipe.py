from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class Recipe(Base):
    __tablename__ = settings.RECIPE_TABLE

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(JSON, nullable=True)

    # N:M
    diet_types = relationship("DietTypeIncluded", back_populates="recipe")
    ingredients = relationship("IngredientsIncluded", back_populates="recipe")
    favourited_by = relationship("RecipeFavourite", back_populates="recipe")
