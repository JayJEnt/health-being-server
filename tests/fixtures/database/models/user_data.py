from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from tests.fixtures.database.supabase_connection import Base
from config import settings


class UserData(Base):
    __tablename__ = settings.USER_DATA_TABLE

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    activity_level = Column(String, nullable=True)
    silhouette = Column(String, nullable=True)

    # 1:1
    user = relationship("User", back_populates="user_data", uselist=False)
