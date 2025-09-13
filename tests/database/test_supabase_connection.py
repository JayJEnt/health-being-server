import pytest


def test_invalid_connection(mocked_supabase_connection_error, example_users_injection):
    with pytest.raises(Exception) as e_info:
        mocked_supabase_connection_error.fetch_all("users")

    assert str(e_info.value) == "500: Internal server error"
