import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_users_create():
    return [
        {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "Password",
            "role": "user",
            "height": 180.0,
            "weight": 75.0,
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "Password",
            "role": "user",
        },
        {
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "Password",
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
            "hashed_password": "Password",
            "role": "user",
            "height": 180.0,
            "weight": 75.0,
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "id": 2,
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "Password",
            "role": "user",
            "activity_level": None,
            "age": None,
            "height": None,
            "weight": None,
            "silhouette": None,
        },
        {
            "id": 3,
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "Password",
            "role": "admin",
            "activity_level": None,
            "age": None,
            "height": None,
            "weight": None,
            "silhouette": None,
        },
    ]


@pytest.fixture()
def example_users_update():
    return [
        {
            "username": "Changed",
            "email": "test@example.com",
            "password": "Password",
            "role": "user",
        },
        {
            "username": "New User",
            "email": "changed@example.com",
            "password": "Password",
            "role": "user",
        },
        {
            "username": "New Admin",
            "email": "newadmin@changed.com",
            "password": "Password",
            "role": "admin",
        },
    ]


@pytest.fixture()
def example_users_response_update():
    return [
        {
            "id": 1,
            "username": "Changed",
            "email": "test@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
            "height": 180.0,
            "weight": 75.0,
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "id": 2,
            "username": "New User",
            "email": "changed@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
            "activity_level": None,
            "age": None,
            "height": None,
            "weight": None,
            "silhouette": None,
        },
        {
            "id": 3,
            "username": "New Admin",
            "email": "newadmin@changed.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "admin",
            "activity_level": None,
            "age": None,
            "height": None,
            "weight": None,
            "silhouette": None,
        },
    ]
