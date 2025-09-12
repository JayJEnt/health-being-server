from pydantic import BaseModel, EmailStr

from typing import Optional


"""UserData models"""


class UserDataCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[str] = (
        None  # e.g. sedentary, lightly active, moderately active, very active
    )
    silhouette: Optional[str] = None  # e.g. ectomorph, mesomorph, endomorph


"""UserData response models"""


class UserData(UserDataCreate):
    user_id: int


"""User models"""


class UserBaseModel(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBaseModel):
    password: str


class UserUpdateAdmin(UserCreate):
    role: str


"""User models"""


class User(UserBaseModel):
    id: int
    role: str = "user"


class UserOurAuth(User):
    hashed_password: str


"""User postcreate models"""


class UserPostCreate(User):
    user_data: Optional[UserData]
