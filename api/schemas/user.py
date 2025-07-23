from pydantic import BaseModel

from datetime import datetime


class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    username: str
    email: str
    password: str