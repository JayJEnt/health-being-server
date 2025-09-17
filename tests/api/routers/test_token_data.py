import pytest

from api.routers.token_data import (
    get_token_owner,
    is_user_an_admin,
)
from api.schemas.user import UserResponse


@pytest.mark.asyncio
async def test_get_token_owner(
    example_users_response,
):
    requesting_user = UserResponse(**example_users_response[0])

    response = await get_token_owner(requesting_user)

    assert response == UserResponse(**example_users_response[0])

    assert isinstance(response, UserResponse)


@pytest.mark.asyncio
async def test_is_user_an_admin(
    example_users_response,
):
    requesting_user = UserResponse(**example_users_response[0])

    response = await is_user_an_admin(requesting_user)

    assert response is False

    assert isinstance(response, bool)
