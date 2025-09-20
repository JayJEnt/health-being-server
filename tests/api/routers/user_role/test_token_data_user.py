import pytest

from api.routers.user_role.token_data_user import get_token_data
from api.schemas.user import User


@pytest.mark.asyncio
async def get_token_data_owner(
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
