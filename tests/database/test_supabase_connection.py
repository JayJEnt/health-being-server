import pytest


def test_connection(mocked_supabase_connection, inject_example_users):
    retrieved_users = mocked_supabase_connection.fetch_all("users")

    assert retrieved_users == inject_example_users


def test_invalid_connection(mocked_supabase_connection_error, inject_example_users):
    with pytest.raises(Exception) as e_info:
        mocked_supabase_connection_error.fetch_all("users")

    assert str(e_info.value) == "500: Internal server error"
