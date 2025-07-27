from pydantic import BaseModel


class VitaminCreate(BaseModel):
    name: str

class Vitamin(VitaminCreate):
    id: int