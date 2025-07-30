from pydantic import BaseModel


class UserBaseModel(BaseModel):
    username: str
    email: str

class UserCreate(UserBaseModel):
    password: str

class User(UserBaseModel):
    id: int
    hashed_password: str
    role: str = "user"