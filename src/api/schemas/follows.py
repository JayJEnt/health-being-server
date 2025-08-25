from pydantic import BaseModel


"""Follows models"""
class CreateFollows(BaseModel):
    username: str