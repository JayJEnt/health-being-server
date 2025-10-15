from pydantic import BaseModel, EmailStr

from typing import Optional

from api.schemas.enum_utils import ActivityLevel, Role, Silhouette


class UserBaseModel(BaseModel):
    username: str
    email: EmailStr
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    silhouette: Optional[Silhouette] = None


class UserCreate(UserBaseModel):
    password: str


class UserUpdateAdmin(UserCreate):
    role: str


class User(UserBaseModel):
    id: int
    role: Role = None


class UserOurAuth(User):
    hashed_password: str


class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    silhouette: Optional[Silhouette] = None
