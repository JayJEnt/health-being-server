import pytest

from api.routers.admin_role.users_admin import (
    get_users,
    update_user,
    delete_user,
)
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_users(
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    response = await get_users()

    assert response == example_users_response
    assert isinstance(response, list)

    for item in response:
        parsed = User(**item)

        assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_get_user(
    mock_supabase_connection,
    example_users_injection,
    example_users_data_injection,
    example_users_response,
):
    response = await get_users(user_id=1)

    assert response == example_users_response[0]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_get_user_by_name(
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    response = await get_users(username="New Admin")

    assert response == example_users_response[2]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_update_user(
    mock_supabase_connection,
    mock_bcrypt,
    example_users_injection,
    example_users_update,
    example_users_response_update,
):
    response = await update_user(user_id=1, user=example_users_update[0])

    assert response == example_users_response_update[0]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_delete_user(
    mock_supabase_connection,
    example_users_injection,
    example_users_data_injection,
    example_users_response,
):
    response = await delete_user(user_id=1)

    assert response == example_users_response[0]

    parsed = User(**response)

    assert isinstance(parsed, User)
