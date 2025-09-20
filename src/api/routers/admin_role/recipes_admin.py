"""/recipes router"""

from fastapi import APIRouter

from api.crud.crud_operations import CrudOperations


router = APIRouter(prefix="/recipes", tags=["admin: recipes"])
crud = CrudOperations("recipes")

# TODO: Add admin routers
