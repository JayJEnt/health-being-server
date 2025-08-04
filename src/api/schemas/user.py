from pydantic import BaseModel, EmailStr

from typing import Optional


class UserBaseModel(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBaseModel):
    password: str

class User(UserBaseModel):
    id: int
    role: str = "user"

class UserOurAuthentication(User):
    hashed_password: str