from pydantic import BaseModel

from typing import Optional

from api.schemas.enum_utils import ActivityLevel, Silhouette


"""UserData models"""


class UserDataCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    silhouette: Optional[Silhouette] = None


"""UserData response models"""


class UserData(UserDataCreate):
    user_id: int
