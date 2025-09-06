import pytest


@pytest.fixture()
def inject_example_ingredients(mocked_supabase_connection_create):
    ingredients = [
        {"name": "Lemon"},
        {"name": "Milk"},
    ]

    return [
        mocked_supabase_connection_create.insert("ingredients", ingredient)
        for ingredient in ingredients
    ]
