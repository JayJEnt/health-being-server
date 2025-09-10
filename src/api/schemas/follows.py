from pydantic import BaseModel


"""Follows models"""


class CreateFollows(BaseModel):
    username: str


class Follows(BaseModel):
    user_id: int
    followed_user_id: int
