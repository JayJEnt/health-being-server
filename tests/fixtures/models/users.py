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


@pytest.fixture()
def example_users_response_all():
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "password",
        "role": "user",
        "user_id": 1,
        "height": "180",
        "weight": "75",
        "age": 25,
        "activity_level": "moderate",
        "silhouette": "mesomorph",
    }


@pytest.fixture()
def example_users_create_all(example_users_create, example_users_data_create):
    for index in range(len(example_users_create)):
        example_users_create[index]["users_data"] = example_users_data_create[index]
    return example_users_create


@pytest.fixture()
def example_users_response_create_all():
    return None


@pytest.fixture()
def example_users_update():
    return [
        {
            "username": "Changed",
            "email": "test@example.com",
            "password": "password",
            "role": "user",
        },
        {
            "username": "New User",
            "email": "changed@example.com",
            "password": "securepassword123",
            "role": "user",
        },
        {
            "username": "New Admin",
            "email": "newadmin@changed.com",
            "password": "securepassword123",
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
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVseizT.QD4DobhKzgJbte/WZRoNvmd3QbK",
            "role": "user",
        },
        {
            "id": 2,
            "username": "New User",
            "email": "changed@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVseizT.QD4DobhKzgJbte/WZRoNvmd3QbK",
            "role": "user",
        },
        {
            "id": 3,
            "username": "New Admin",
            "email": "newadmin@changed.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVseizT.QD4DobhKzgJbte/WZRoNvmd3QbK",
            "role": "admin",
        },
    ]
