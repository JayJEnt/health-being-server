from fastapi import Depends

from typing import Annotated

from api.schemas.user import User
from api.authentication.token import validate_token
from api.handlers.exceptions import DemandAdminAccess, DemandBeingLogged


async def admin_only(user: Annotated[User, Depends(validate_token)]):
    if user["role"] != "admin":
        raise DemandAdminAccess

async def logged_only(user: Annotated[User, Depends(validate_token)]):
    if not user:
        raise DemandBeingLogged
