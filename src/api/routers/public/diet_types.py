"""/diet_types router"""

from fastapi import APIRouter

from typing import List

from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.diet_type import DietType


router = APIRouter(prefix="/diet_types", tags=["public: diet_types"])
crud = CrudOperations("diet_type")


@router.get("", response_model=List[DietType])
async def get_diet_types():
    return await crud.get()


@router.get("/", response_model=DietType)
async def get_diet_type(diet_type_id: int = None, diet_name: str = None):
    if diet_type_id:
        return await crud.get_by_id(diet_type_id)
    if diet_name:
        return await crud.get_by_name(diet_name)
    raise DemandQueryParameter
