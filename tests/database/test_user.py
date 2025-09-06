import pytest


def test_post_users(mocked_supabase_connection_create, inject_example_users):
    retrieved_users = mocked_supabase_connection_create.fetch_all("users")

    assert retrieved_users == inject_example_users


def test_delete_user(mocked_supabase_connection_create, inject_example_users):
    mocked_supabase_connection_create.delete_by(
        "users", "id", inject_example_users[0]["id"]
    )

    retrieved_users = mocked_supabase_connection_create.fetch_all("users")

    assert retrieved_users == inject_example_users[1:]


def test_find_user_by(mocked_supabase_connection_create, inject_example_users):
    retrieved_user = mocked_supabase_connection_create.find_by(
        "users", "username", "testuser2"
    )

    assert retrieved_user == [inject_example_users[1]]


def test_find_user_ilike(mocked_supabase_connection_create, inject_example_users):
    retrieved_users = mocked_supabase_connection_create.find_ilike(
        "users", "username", "TESTUSER"
    )

    assert retrieved_users == inject_example_users


def test_update_user(mocked_supabase_connection_create, inject_example_users):
    assert inject_example_users[0]["role"] == "user"

    updates = {"role": "admin"}
    mocked_supabase_connection_create.update_by(
        "users", "id", inject_example_users[0]["id"], updates
    )

    retrieved_user = mocked_supabase_connection_create.find_by(
        "users", "id", inject_example_users[0]["id"]
    )

    assert retrieved_user[0]["role"] == "admin"


def test_find_user_error(mocked_supabase_connection_create, inject_example_users):
    with pytest.raises(Exception) as e_info:
        mocked_supabase_connection_create.find_by("users", "id", 999)

    assert str(e_info.value) == "404: Requested resource not found"
