import pytest

from api.routers.user_role.users_data_user import (
    get_owner_data,
    update_owner_data,
    delete_owner_data,
)
from api.schemas.user_data import UserDataCreate, UserData
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_response,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await get_owner_data(requesting_user)

    assert response == example_users_data_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)


@pytest.mark.asyncio
async def test_update_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_update,
    example_users_data_update_response,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    user_data = UserDataCreate(**example_users_data_update[0])
    response = await update_owner_data(user_data, requesting_user)

    assert response == example_users_data_update_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)


@pytest.mark.asyncio
async def test_delete_user_data(
    mock_supabase_connection,
    example_users_data_injection,
    example_users_data_response,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await delete_owner_data(requesting_user)

    assert response == example_users_data_response[0]

    parsed = UserData(**response)

    assert isinstance(parsed, UserData)
