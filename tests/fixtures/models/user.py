import pytest


@pytest.fixture()
def inject_example_users(mocked_supabase_connection):
    users = [
        {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": "password",
            "role": "user",
        },
        {
            "username": "testuser2",
            "email": "test2@example.com",
            "hashed_password": "password",
            "role": "user",
        },
        {
            "username": "testuser3",
            "email": "test3@example.com",
            "hashed_password": "password",
            "role": "admin",
        },
    ]

    return [mocked_supabase_connection.insert("users", user) for user in users]
