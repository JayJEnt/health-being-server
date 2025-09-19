import pytest

from api.routers.user_role.token_data_user import (
    get_token_owner,
    is_user_an_admin,
)
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_token_owner(
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await get_token_owner(requesting_user)

    assert response == User(**example_users_response[0])

    assert isinstance(response, User)


@pytest.mark.asyncio
async def test_is_user_an_admin(
    example_users_response,
):
    requesting_user = User(**example_users_response[0])

    response = await is_user_an_admin(requesting_user)

    assert response is False

    assert isinstance(response, bool)
