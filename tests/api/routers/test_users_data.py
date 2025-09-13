import pytest

from api.routers.users_data import (
    get_user_data,
    update_user_data,
    delete_user_data,
)
from api.schemas.user_data import UserDataCreate, UserData


@pytest.mark.asyncio
async def test_get_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_response,
):
    response = await get_user_data(1)

    assert response == example_users_data_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)


@pytest.mark.asyncio
async def test_update_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_update,
    example_users_data_update_response,
):
    user_data = UserDataCreate(**example_users_data_update[0])
    response = await update_user_data(1, user_data)

    assert response == example_users_data_update_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)


@pytest.mark.asyncio
async def test_delete_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_response,
):
    response = await delete_user_data(1)

    assert response == example_users_data_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)
