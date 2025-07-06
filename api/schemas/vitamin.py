from pydantic import BaseModel


class Vitamin(BaseModel):
    id: int
    name: str