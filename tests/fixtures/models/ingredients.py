import pytest


@pytest.fixture()
def inject_example_ingredients(mocked_supabase_connection):
    ingredients = [
        {"name": "Lemon"},
        {"name": "Milk"},
    ]

    return [mocked_supabase_connection.insert("ingredients", ingredient) for ingredient in ingredients]