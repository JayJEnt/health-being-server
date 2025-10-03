from pydantic import BaseModel


class DietTypeCreate(BaseModel):
    diet_name: str


class DietTypeResponse(DietTypeCreate):
    id: int
