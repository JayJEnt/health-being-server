from pydantic import BaseModel


class CreateVitamin(BaseModel):
    name: str

class Vitamin(CreateVitamin):
    id: int