"""/users router"""

from fastapi import APIRouter, Depends

from api.schemas.user import User, UserCreate, UserPatch
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


@router.patch("", response_model=User, dependencies=[Depends(logged_only)])
async def patch_owner(
    user_update: UserPatch, requesting_user: User = Depends(validate_token)
):
    if user_update.password:
        user_update = await hash_pass_for_user(user_update)
    else:
        user_update = user_update.model_dump()

    clean_data = {k: v for k, v in user_update.items() if v is not None}

    print(f"clean_data: {clean_data}")
    return await crud.put(requesting_user.id, clean_data)


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
