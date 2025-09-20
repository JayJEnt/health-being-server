"""/vitamins router"""

from fastapi import APIRouter

from typing import List

from api.crud.crud_operations import CrudOperations
from api.handlers.exceptions import DemandQueryParameter
from api.schemas.vitamin import Vitamin


router = APIRouter(prefix="/vitamins", tags=["public: vitamins"])
crud = CrudOperations("vitamins")


@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    return await crud.get()


@router.get("/", response_model=Vitamin)
async def get_vitamin(vitamin_id: int = None, vitamin_name: str = None):
    if vitamin_id:
        return await crud.get_by_id(vitamin_id)
    if vitamin_name:
        return await crud.get_by_name(vitamin_name)
    raise DemandQueryParameter
