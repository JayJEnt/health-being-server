from pydantic import BaseModel, EmailStr


class UserBaseModel(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBaseModel):
    password: str

class User(UserBaseModel):
    id: int
    hashed_password: str
    role: str = "user"