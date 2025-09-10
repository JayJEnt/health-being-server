import pytest

from api.routers.users import (
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_by_name,
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
    example_users_response_all,
):
    response = await get_user(1)

    assert response == example_users_response_all

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_get_user_by_name(
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    response = await get_user_by_name("New Admin")

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
    response = await update_user(1, example_users_update[0])

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
    response = await delete_user(1)

    assert response == example_users_response[0]

    parsed = User(**response)

    assert isinstance(parsed, User)
