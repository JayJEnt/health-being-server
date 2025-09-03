from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class PreferedRecipeType(Base):
    __tablename__ = settings.PREFERED_RECIPE_TYPE_TABLE

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    type_id = Column(Integer, ForeignKey("diet_types.id"), primary_key=True)

    user = relationship("User", back_populates="diet_types")
    diet_type = relationship("DietType", back_populates="users")
