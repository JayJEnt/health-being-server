"""/diet_types router"""

from fastapi import APIRouter

from typing import List, Union

from api.crud.crud_operations import CrudOperations
from api.schemas.diet_type import DietType


router = APIRouter(prefix="/diet_types", tags=["public: diet_types"])
crud = CrudOperations("diet_type")


@router.get("", response_model=Union[DietType, List[DietType]])
async def get_diet_types(diet_type_id: int = None, diet_name: str = None):
    if diet_type_id:
        return await crud.get_by_id(diet_type_id)
    if diet_name:
        return await crud.get_by_name(diet_name)
    return await crud.get()
