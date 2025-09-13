from pydantic import BaseModel, EmailStr

from api.schemas.user_data import UserDataCreate


"""User Create models"""


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


"""User with UserData models"""


class UserCreateAll(User, UserDataCreate):
    pass
