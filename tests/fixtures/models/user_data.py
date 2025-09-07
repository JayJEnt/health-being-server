import pytest


@pytest.fixture()
def inject_example_users_data(mocked_supabase_connection):
    users_data = [
        {
            "user_id": "1",
            "height": 180,
            "weight": 75,
            "age": 25,
            "activity_level": "moderate",
        },
        {
            "user_id": "2",
            "height": 165,
            "weight": 68,
            "age": 30,
            "activity_level": "active",
        },
    ]

    return [
        mocked_supabase_connection.insert("user_data", user_data)
        for user_data in users_data
    ]
