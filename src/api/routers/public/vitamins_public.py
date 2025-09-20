"""/vitamins router"""

from fastapi import APIRouter

from typing import List, Union

from api.crud.crud_operations import CrudOperations
from api.schemas.vitamin import Vitamin


router = APIRouter(prefix="/vitamins", tags=["public: vitamins"])
crud = CrudOperations("vitamins")


@router.get("", response_model=Union[Vitamin, List[Vitamin]])
async def get_vitamins(vitamin_id: int = None, vitamin_name: str = None):
    if vitamin_id:
        return await crud.get_by_id(vitamin_id)
    if vitamin_name:
        return await crud.get_by_name(vitamin_name)
    return await crud.get()
