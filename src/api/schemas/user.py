from pydantic import BaseModel, EmailStr

from api.schemas.user_data import UserDataCreate
from api.schemas.enum_utils import Role


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
    role: Role = Role.user.value


class UserOurAuth(User):
    hashed_password: str


"""User with UserData models"""


class UserCreateAll(User, UserDataCreate):
    pass
