import pytest

from api.authentication.allowed_roles import admin_only, logged_only, owner_only
from api.schemas.user import User


@pytest.mark.asyncio
async def test_admin_only(example_users_response):
    requesting_user = User(**example_users_response[2])
    await admin_only(requesting_user)

    assert True  # If passes, then its good


@pytest.mark.asyncio
async def test_admin_only_error(example_users_response):
    requesting_user = User(**example_users_response[0])
    with pytest.raises(Exception) as excinfo:
        await admin_only(requesting_user)

    assert str(excinfo.value) == "401: You need admin access for this action"


@pytest.mark.asyncio
async def test_logged_only(example_users_response):
    requesting_user = User(**example_users_response[2])
    await logged_only(requesting_user)

    assert True  # If passes, then its good


@pytest.mark.asyncio
async def test_logged_only_error(example_users_response):
    with pytest.raises(Exception) as excinfo:
        await logged_only(None)

    assert str(excinfo.value) == "401: You need to be logged in for this action"


@pytest.mark.asyncio
async def test_owner_only(
    mock_supabase_connection, example_users_response, example_recipes_injection
):
    requesting_user = User(**example_users_response[0])
    await owner_only("recipes", 1, requesting_user)

    assert True  # If passes, then its good


@pytest.mark.asyncio
async def test_owner_only_error(
    mock_supabase_connection, example_users_response, example_recipes_injection
):
    requesting_user = User(**example_users_response[2])
    with pytest.raises(Exception) as excinfo:
        await owner_only("recipes", 1, requesting_user)

    assert (
        str(excinfo.value) == "401: You can perform this action only at your own data"
    )
