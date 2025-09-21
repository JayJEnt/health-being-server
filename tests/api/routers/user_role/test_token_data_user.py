import pytest

from api.routers.user_role.token_data_user import get_token_data, refresh_token
from api.schemas.user import User
from api.schemas.token import Token


@pytest.mark.asyncio
async def test_get_token_data(
    example_users_response,
):
    user = User(**example_users_response[0])

    response = await get_token_data(user=user)

    assert response == User(**example_users_response[0])

    assert isinstance(response, User)


@pytest.mark.asyncio
async def test_is_user_an_admin(
    example_users_response,
):
    user = User(**example_users_response[0])

    response = await get_token_data(user=user, admin_role=True)

    assert response is False

    assert isinstance(response, bool)


@pytest.mark.asyncio
async def test_refresh_token(
    expected_token,
):
    token = Token(**{"access_token": expected_token, "token_type": "bearer"})

    response = await refresh_token(token=token)

    assert response == token

    assert isinstance(response, Token)
