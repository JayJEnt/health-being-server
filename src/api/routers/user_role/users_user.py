"""/users router"""

from fastapi import APIRouter, Depends

from api.schemas.user import User, UserCreate
from api.authentication.allowed_roles import logged_only
from api.crud.crud_operations import CrudOperations
from api.authentication.token import validate_token
from api.authentication.oauth2_our import hash_pass_for_user


router = APIRouter(prefix="/users/owner", tags=["user: users"])
crud = CrudOperations("user")


@router.get("", response_model=User, dependencies=[Depends(logged_only)])
async def get_owner(requesting_user: User = Depends(validate_token)):
    return await crud.get_all(requesting_user.id)


@router.put("", response_model=User, dependencies=[Depends(logged_only)])
async def update_owner(
    user: UserCreate, requesting_user: User = Depends(validate_token)
):
    user = await hash_pass_for_user(user)
    return await crud.put_all(requesting_user.id, user)


@router.delete("", response_model=User, dependencies=[Depends(logged_only)])
async def delete_owner(requesting_user: User = Depends(validate_token)):
    return await crud.delete_all(
        requesting_user.id,
        related_attributes=[
            "user",
            "ingredients",
            "diet_type",
            "recipes",
            "refrigerator",
        ],
    )
