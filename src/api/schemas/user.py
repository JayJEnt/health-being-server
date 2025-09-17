from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from api.schemas.nested.user_data import UserDataCreate
from api.schemas.enum_utils import Role


class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)


class UserCreate(UserBase):
    password: str = Field(nullable=False)


class UserUpdateAdmin(UserCreate):
    role: Role = Field(default=Role.user.value, nullable=False)


class UserDB(UserCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(default=None, nullable=True)
    role: Role = Field(default=Role.user.value, nullable=False)


class UserResponse(UserBase):
    id: int
    role: Role


class UserOurAuth(UserResponse):
    hashed_password: str


class UserResponseAll(UserResponse, UserDataCreate):
    pass
