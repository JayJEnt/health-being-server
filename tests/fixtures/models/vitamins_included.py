import pytest


@pytest.fixture()
def inject_example_vitamins_included(mocked_supabase_connection):
    vitamins_included = [
        {
            "ingredient_id": "1",
            "vitamin_id": "1",
        },
        {
            "ingredient_id": "2",
            "vitamin_id": "2",
        }
    ]

    return [mocked_supabase_connection.insert("vitamins_included", vitamin) for vitamin in vitamins_included]