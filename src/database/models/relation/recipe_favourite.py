from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class RecipeFavourite(Base):
    __tablename__ = settings.RECIPE_FAVOURITE

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    recipe = relationship("Recipe", back_populates="favourited_by")
    user = relationship("User", back_populates="recipes")
