import pytest
import pytest_asyncio

from api.crud.relation.post_methods import create_relationship


@pytest.fixture()
def example_follows_create():
    return [
        {
            "username": "New User",
        },
    ]


@pytest_asyncio.fixture
async def example_follows_injection(
    mock_supabase_connection,
    example_follows_create,
    example_users_injection,
):
    for user in example_follows_create:
        await create_relationship("user", 1, "user", user)


@pytest.fixture()
def example_follows_create_response():
    return [
        {"followed_user_id": 2, "username": "New User"},
    ]


@pytest.fixture()
def example_follows_response():
    return [
        {"user_id": 1, "followed_user_id": 2},
    ]


@pytest.fixture()
def example_follows_name_response():
    return [
        {
            "followed_user_id": 2,
            "username": "New User",
        },
    ]


@pytest.fixture()
def example_follows_update():
    return [
        {
            "username": "New Admin",
        },
    ]


@pytest.fixture()
def example_follows_update_response():
    return [
        {"followed_user_id": 3, "username": "New Admin"},
    ]
