from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.supabase_connection import Base
from config import settings


class User(Base):
    __tablename__ = settings.USER_TABLE

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")

    # 1:1
    user_data = relationship("UserData", back_populates="user", uselist=False)

    # N:M
    recipes = relationship("RecipeFavourite", back_populates="user")
    ingredients = relationship("PreferedIngredients", back_populates="user")
    diet_types = relationship("PreferedRecipeType", back_populates="user")
    refrigerator = relationship("Refrigerator", back_populates="user")
    follows = relationship(
        "Follow", foreign_keys="[Follow.user_id]", back_populates="user"
    )
    followers = relationship(
        "Follow",
        foreign_keys="[Follow.followed_user_id]",
        back_populates="followed_user",
    )
