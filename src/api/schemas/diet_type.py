from pydantic import BaseModel


class DietTypeCreate(BaseModel):
    diet_name: str

class DietType(DietTypeCreate):
    id: int