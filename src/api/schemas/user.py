from pydantic import BaseModel, EmailStr

from typing import Optional


"""User models"""
class UserBaseModel(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBaseModel):
    password: str

class User(UserBaseModel):
    id: int
    role: str = "user"

class UserOurAuth(User):
    hashed_password: str




"""UserData models"""
class UserDataCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[str] = None  # e.g. sedentary, lightly active, moderately active, very active
    sillouette: Optional[str] = None  # e.g. ectomorph, mesomorph, endomorph

class UserData(UserDataCreate):
    user_id: int




"""FullUser models"""
class FullUser(User, UserDataCreate):
    pass
