from pydantic import BaseModel

from typing import Optional


"""UserData models"""


class UserDataCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[str] = (
        None  # e.g. sedentary, lightly active, moderately active, very active
    )
    silhouette: Optional[str] = None  # e.g. ectomorph, mesomorph, endomorph


"""UserData response models"""


class UserData(UserDataCreate):
    user_id: int
