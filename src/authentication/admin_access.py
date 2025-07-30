from fastapi import HTTPException, status, Depends

from functools import wraps
from typing import Callable

from src.authentication.authentication import get_current_user_role


def only_admin_allowed(func: Callable):
    @wraps(func)
    async def wrapper(
        *args,
        user_role: str = Depends(get_current_user_role),
        **kwargs
    ):
        credential_unaccepted = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need admin access for this action",
            headers={"WWW-Authenticate": "Bearer"}
        )
        if user_role != "admin":
            raise credential_unaccepted
        return await func(*args, **kwargs)
    return wrapper