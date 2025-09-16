import pytest
import pytest_asyncio

from api.crud.relation.post_methods import create_relationship


@pytest.fixture()
def example_prefered_ingredients_create():
    return [
        {
            "name": "Carrot",
            "preference": "alergic to",
        },
    ]


@pytest_asyncio.fixture
async def example_prefered_ingredients_injection(
    mock_supabase_connection,
    example_prefered_ingredients_create,
    example_users_injection,
    example_ingredients_injection,
):
    for ingredient in example_prefered_ingredients_create:
        await create_relationship("user", 1, "ingredients", ingredient)


@pytest.fixture()
def example_prefered_ingredients_create_response():
    return [
        {"id": 2, "name": "Carrot", "preference": "alergic to"},
    ]


@pytest.fixture()
def example_prefered_ingredients_response():
    return [
        {"user_id": 1, "ingredient_id": 2, "preference": "alergic to"},
    ]


@pytest.fixture()
def example_prefered_ingredients_name_response():
    return [
        {"ingredient_id": 2, "name": "Carrot", "preference": "alergic to"},
    ]


@pytest.fixture()
def example_prefered_ingredients_update():
    return [
        {
            "name": "Carrot",
            "preference": "like",
        },
    ]


@pytest.fixture()
def example_prefered_ingredients_update_response():
    return [
        {"user_id": 1, "name": "Carrot", "preference": "like"},
    ]
