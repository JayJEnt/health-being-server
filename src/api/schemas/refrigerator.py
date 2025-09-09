from pydantic import BaseModel


class CreateRefrigerator(BaseModel):
    name: str
    amount: int


class PostCreateRefrigerator(CreateRefrigerator):
    id: int


class Refrigerator(BaseModel):
    user_id: int
    ingredient_id: int
    amount: int
