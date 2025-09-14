import pytest

from api.routers.follows import (
    get_all_relations_follows,
    create_relation_follows,
    get_relation_follows,
    delete_relation_follows,
)
from api.schemas.follows import Follows, CreateFollows, FollowsGet
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_all_relations_follows(
    mock_supabase_connection,
    example_follows_injection,
    example_users_response,
    example_follows_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_all_relations_follows(requesting_user)

    assert response == example_follows_response

    for item in response:
        parsed = Follows(**item)

        assert isinstance(parsed, Follows)


@pytest.mark.asyncio
async def test_create_relation_follows(
    mock_supabase_connection,
    example_users_injection,
    example_follows_create,
    example_users_response,
):
    requesting_user = User(**example_users_response[0])
    followed_user = CreateFollows(**example_follows_create[0])
    response = await create_relation_follows(followed_user, requesting_user)

    assert response == example_users_response[1]

    parsed = User(**response)

    assert isinstance(parsed, User)


@pytest.mark.asyncio
async def test_get_relation_follows(
    mock_supabase_connection,
    example_follows_injection,
    example_users_response,
    example_follows_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_follows(2, requesting_user)

    assert response == example_follows_name_response[0]

    parsed = FollowsGet(**response)

    assert isinstance(parsed, FollowsGet)


@pytest.mark.asyncio
async def test_delete_relation_follows(
    mock_supabase_connection,
    example_follows_injection,
    example_users_response,
    example_follows_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_relation_follows(2, requesting_user)

    assert response == example_follows_response[0]

    parsed = Follows(**response)

    assert isinstance(parsed, Follows)
