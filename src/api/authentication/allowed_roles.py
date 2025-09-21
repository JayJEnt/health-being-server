from fastapi import Depends

from typing import Annotated

from api.schemas.user import User
from api.crud.single_entity.get_methods import get_element_by_id
from api.authentication.token import validate_token
from api.handlers.http_exceptions import (
    DemandAdminAccess,
    DemandBeingLogged,
    DemandOwnerAccess,
)


async def admin_only(user: Annotated[User, Depends(validate_token)]):
    if user.role != "admin":
        raise DemandAdminAccess


async def logged_only(user: Annotated[User, Depends(validate_token)]):
    if not user:
        raise DemandBeingLogged


async def owner_only(element_type: str, element_id: int, user: User):
    user_id_names_mapping = {
        "recipes": "owner_id",
    }
    element_response = await get_element_by_id(element_type, element_id)
    if element_response[user_id_names_mapping[element_type]] != user.id:
        raise DemandOwnerAccess
