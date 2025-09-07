import pytest
import pytest_asyncio


@pytest.fixture()
def example_ingredients_create():
    return [
        {"name": "Bread"},
        {"name": "Carrot"},
        {"name": "Mushroom"},
        {"name": "Rice"},
    ]


@pytest_asyncio.fixture
async def example_ingredients_injection(
    mock_supabase_connection, example_ingredients_create
):
    from api.crud.single_entity.post_methods import create_element

    for ingredient in example_ingredients_create:
        await create_element("ingredients", ingredient)


@pytest.fixture()
def example_ingredients_response():
    return [
        {"id": 1, "name": "Bread"},
        {"id": 2, "name": "Carrot"},
        {"id": 3, "name": "Mushroom"},
        {"id": 4, "name": "Rice"},
    ]
