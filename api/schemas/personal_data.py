from pydantic import BaseModel
from typing import Optional


class CreatePersonalData(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[str] = None  # e.g. sedentary, lightly active, moderately active, very active
    sillouette: Optional[str] = None  # e.g. ectomorph, mesomorph, endomorph

class PersonalData(CreatePersonalData):
    user_id: int