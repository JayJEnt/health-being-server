def test_post_user_data(mocked_supabase_connection, inject_example_users_data):
    retrieved_user_data = mocked_supabase_connection.find_by(
        "user_data",
        "user_id",
        inject_example_users_data[0]["user_id"]
    )

    assert retrieved_user_data == [inject_example_users_data[0]]


def test_delete_user_data(mocked_supabase_connection, inject_example_users_data):
    mocked_supabase_connection.delete_by(
        "user_data",
        "user_id",
        inject_example_users_data[0]["user_id"]
    )

    retrieved_user_data = mocked_supabase_connection.fetch_all("user_data")

    assert retrieved_user_data == [inject_example_users_data[1]]


def test_find_user_data_by(mocked_supabase_connection, inject_example_users_data):
    retrieved_user_data = mocked_supabase_connection.find_by(
        "user_data",
        "user_id",
        inject_example_users_data[0]["user_id"]
    )

    assert retrieved_user_data == [inject_example_users_data[0]]


def test_update_user_data(mocked_supabase_connection, inject_example_users_data):
    assert inject_example_users_data[0]["height"] == '180'

    updates = {"height": 185}
    mocked_supabase_connection.update_by(
        "user_data",
        "user_id",
        inject_example_users_data[0]["user_id"],
        updates
    )

    retrieved_user_data = mocked_supabase_connection.find_by(
        "user_data",
        "user_id",
        inject_example_users_data[0]["user_id"]
    )

    assert retrieved_user_data[0]["height"] == '185'