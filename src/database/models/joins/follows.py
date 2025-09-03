from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class Follow(Base):
    __tablename__ = settings.FOLLOW_TABLE

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="follows")
    followed_user = relationship("User", foreign_keys=[followed_user_id], back_populates="followers")
