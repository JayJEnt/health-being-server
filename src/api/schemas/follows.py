from pydantic import BaseModel


class FollowsCreate(BaseModel):
    username: str


class Follows(FollowsCreate):
    followed_user_id: int


class FollowsDelete(BaseModel):
    followed_user_id: int
    user_id: int
