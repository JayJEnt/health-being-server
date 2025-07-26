from pydantic import BaseModel


class CreateDietType(BaseModel):
    diet_name: str

class DietType(CreateDietType):
    id: int