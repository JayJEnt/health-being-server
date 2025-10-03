"""/diet_types router"""

from fastapi import APIRouter, Depends

from api.authentication.allowed_roles import admin_only
from api.crud.crud_operations import CrudOperations
from api.schemas.diet_type import DietTypeCreate, DietTypeResponse


router = APIRouter(prefix="/diet_types", tags=["admin: diet_types"])
crud = CrudOperations("diet_type")


@router.post("", response_model=DietTypeResponse, dependencies=[Depends(admin_only)])
async def create_diet_type(diet_type: DietTypeCreate):
    return await crud.post(diet_type)


@router.put("", response_model=DietTypeResponse, dependencies=[Depends(admin_only)])
async def update_diet_type(diet_type: DietTypeCreate, diet_type_id: int):
    return await crud.put(diet_type_id, diet_type)


@router.delete("", response_model=DietTypeResponse, dependencies=[Depends(admin_only)])
async def delete_diet_type(diet_type_id: int):
    return await crud.delete(diet_type_id)
