from sqlmodel import Field, SQLModel

from typing import Optional

# from api.schemas import VitaminsIncludedDB
from config import settings


class VitaminBase(SQLModel):
    name: str = Field(unique=True, nullable=False)


class VitaminCreate(VitaminBase):
    pass


class VitaminDB(VitaminBase, table=True):
    __tablename__ = settings.VITAMIN_TABLE

    id: Optional[int] = Field(default=None, primary_key=True)

    # ingredients: List[VitaminsIncludedDB] = Relationship(back_populates="vitamin")


class VitaminResponse(VitaminBase):
    id: int
