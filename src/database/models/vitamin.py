from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class Vitamin(Base):
    __tablename__ = settings.VITAMIN_TABLE

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # N:M
    ingredients = relationship("VitaminsIncluded", back_populates="vitamin")
