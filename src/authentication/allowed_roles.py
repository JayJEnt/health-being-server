from fastapi import Depends

from typing import Annotated

from api.schemas.user import User
from authentication.authentication import validate_token
from api.handlers.exceptions import DemandAdminAccess


async def admin_only(user: Annotated[User, Depends(validate_token)]):
    if user["role"] != "admin":
        raise DemandAdminAccess
