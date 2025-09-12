from fastapi.security import OAuth2PasswordRequestForm

import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_users_hashed_create():
    return [
        {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
        },
        {
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
        },
        {
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "admin",
        },
    ]


@pytest_asyncio.fixture
async def example_users_hashed_injection(
    mock_supabase_connection, example_users_hashed_create
):
    for user in example_users_hashed_create:
        await create_element("user", user)


@pytest.fixture()
def example_users_hashed_response():
    return [
        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
        },
        {
            "id": 2,
            "username": "New User",
            "email": "newuser@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "user",
        },
        {
            "id": 3,
            "username": "New Admin",
            "email": "newadmin@example.com",
            "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
            "role": "admin",
        },
    ]


@pytest.fixture()
def example_form_data():
    return OAuth2PasswordRequestForm(
        username="test@example.com", password="Password", scope=""
    )


@pytest.fixture()
def example_form_data_error():
    return OAuth2PasswordRequestForm(
        username="test@example.com", password="123", scope=""
    )


@pytest.fixture()
def expected_token_our_login():
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0dXNlciIsInN1YiI6InRlc3RAZXhhbXBsZS5jb20iLCJwcm92aWRlciI6ImhlYWx0aC1iZWluZy1zZXJ2ZXIiLCJleHAiOjE2NzM3ODcwMDB9.AscOu7pvqnjspW-Rde_hKbbBJes93CyLVKp9uKI9m3Y",
        "token_type": "bearer",
    }


@pytest.fixture()
def example_users_register():
    return [
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password",
        },
        {
            "username": "New User",
            "email": "newuser@example.com",
            "password": "Password",
        },
        {
            "username": "New Admin",
            "email": "newadmin@example.com",
            "password": "Password",
        },
    ]
