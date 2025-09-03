from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class DietTypeIncluded(Base):
    __tablename__ = settings.DIET_TYPE_INCLUDED_TABLE

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    diet_type_id = Column(Integer, ForeignKey("diet_types.id"), primary_key=True)

    recipe = relationship("Recipe", back_populates="diet_types")
    diet_type = relationship("DietType", back_populates="recipes")
