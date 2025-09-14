import pytest
import pytest_asyncio

from api.crud.relation.post_methods import create_relationship


@pytest.fixture()
def example_recipe_favourite_create():
    return [
        {
            "title": "Healthy Salad",
        },
    ]


@pytest_asyncio.fixture
async def example_recipe_favourite_injection(
    mock_supabase_connection,
    example_recipe_favourite_create,
    example_users_injection,
    example_recipes_injection,
):
    for recipe in example_recipe_favourite_create:
        await create_relationship("user", 1, "recipes", recipe)


@pytest.fixture()
def example_recipe_favourite_create_response():
    return [
        {
            "description": "A fresh and healthy salad.",
            "id": 1,
            "instructions": [
                "Mix all ingredients in a bowl and serve fresh.",
            ],
            "owner_id": 1,
            "title": "Healthy Salad",
        },
    ]


@pytest.fixture()
def example_recipe_favourite_response():
    return [
        {"user_id": 1, "recipe_id": 1},
    ]


@pytest.fixture()
def example_recipe_favourite_names_response():
    return [
        {"recipes": "Healthy Salad", "users": "testuser"},
    ]
