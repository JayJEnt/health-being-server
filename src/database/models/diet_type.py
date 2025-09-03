from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class DietType(Base):
    __tablename__ = settings.DIET_TYPE_TABLE

    id = Column(Integer, primary_key=True, index=True)
    diet_name = Column(String, unique=True, nullable=False)

    # N:M
    recipes = relationship("DietTypeIncluded", back_populates="diet_type")
    users = relationship("PreferedRecipeType", back_populates="diet_type")
