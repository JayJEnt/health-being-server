from pydantic import BaseModel, EmailStr

from typing import Optional

from api.schemas.enum_utils import ActivityLevel, Role, Silhouette


class UserData(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    silhouette: Optional[Silhouette] = None


class UserBaseModel(UserData):
    username: str
    email: EmailStr


class UserCreate(UserBaseModel):
    password: str


class UserUpdateAdmin(UserCreate):
    role: str = Role.unconfirmed.value


class User(UserBaseModel):
    id: int
    role: Role = None


class UserPatch(UserData):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
