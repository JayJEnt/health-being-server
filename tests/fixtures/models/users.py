import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_users_create():
    return [
        {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "password",
            "role": "user",
        },
        {
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "securepassword123",
            "role": "user",
        },
        {
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "securepassword123",
            "role": "admin",
        },
    ]


@pytest_asyncio.fixture
async def example_users_injection(mock_supabase_connection, example_users_create):
    for user in example_users_create:
        await create_element("user", user)


@pytest.fixture()
def example_users_response():
    return [
        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "password",
            "role": "user",
        },
        {
            "id": 2,
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "securepassword123",
            "role": "user",
        },
        {
            "id": 3,
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "securepassword123",
            "role": "admin",
        },
    ]
