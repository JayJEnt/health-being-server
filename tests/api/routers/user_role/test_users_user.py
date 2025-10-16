import pytest

from api.routers.user_role.users_user import (
    get_owner,
    update_owner,
    patch_owner,
    delete_owner,
)
from api.schemas.user import User, UserPatch


@pytest.mark.asyncio
async def test_get_owner(
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await get_owner(requesting_user=requesting_user)

    assert response == example_users_response[0]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_update_owner(
    mock_supabase_connection,
    mock_bcrypt,
    example_users_injection,
    example_users_update,
    example_users_response,
    example_users_response_update,
):
    requesting_user = User(**example_users_response[0])

    response = await update_owner(
        requesting_user=requesting_user, user=example_users_update[0]
    )

    assert response == example_users_response_update[0]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_patch_owner(
    mock_supabase_connection,
    mock_bcrypt,
    example_users_injection,
    example_users_patch,
    example_users_response,
    example_users_response_update,
):
    requesting_user = User(**example_users_response[0])
    user = UserPatch(**example_users_patch[0])

    response = await patch_owner(requesting_user=requesting_user, user=user)

    assert response == example_users_response_update[0]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_delete_owner(
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await delete_owner(requesting_user=requesting_user)

    assert response == example_users_response[0]

    parsed = User(**response)

    assert isinstance(parsed, User)
