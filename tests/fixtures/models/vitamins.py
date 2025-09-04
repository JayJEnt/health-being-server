import pytest


@pytest.fixture()
def inject_example_vitamins(mocked_supabase_connection):
    vitamins = [
        {"name": "C"},
        {"name": "D"},
    ]

    return [mocked_supabase_connection.insert("vitamins", vitamin) for vitamin in vitamins]