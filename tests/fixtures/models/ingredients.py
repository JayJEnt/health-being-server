import pytest


@pytest.fixture()
def example_ingredients_create():
    ingredients_create = [
        {"name": "Bread"},
        {"name": "Lemon"},
        {"name": "Milk"},
        {"name": "Rice"},
    ]
    return ingredients_create


@pytest.fixture()
def inject_example_ingredients(mocked_supabase_connection, example_ingredients_create):
    for ingredient in example_ingredients_create:
        mocked_supabase_connection.insert("ingredients", ingredient)


@pytest.fixture()
def example_ingredients_response():
    ingredients_response = [
        {"id": 1, "name": "Bread"},
        {"id": 2, "name": "Lemon"},
        {"id": 3, "name": "Milk"},
        {"id": 4, "name": "Rice"},
    ]
    return ingredients_response
