from pydantic import BaseModel


class DietaryType(BaseModel):
    id: int
    name: str