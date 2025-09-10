import pytest
import pytest_asyncio

from api.crud.relation.post_methods import create_relationship


@pytest.fixture()
def example_refrigerator_create():
    return [
        {
            "name": "Carrot",
            "amount": 50,
        },
        {
            "name": "Mushroom",
            "amount": 18,
        },
    ]


@pytest_asyncio.fixture
async def example_refrigerator_injection(
    mock_supabase_connection,
    example_refrigerator_create,
    example_ingredients_injection,
    example_users_injection,
):
    for ingredient in example_refrigerator_create:
        await create_relationship("user", 1, "refrigerator", ingredient)


@pytest.fixture()
def example_refrigerator_create_response():
    return [
        {"id": 2, "name": "Carrot", "amount": 50},
        {"id": 3, "name": "Mushroom", "amount": 18},
    ]


@pytest.fixture()
def example_refrigerator_response():
    return [
        {"user_id": 1, "ingredient_id": 2, "amount": 50},
        {"user_id": 1, "ingredient_id": 3, "amount": 18},
    ]


@pytest.fixture()
def example_refrigerator_update():
    return [
        {
            "name": "Carrot",
            "amount": 10,
        },
        {
            "name": "Bread",
            "amount": 1,
        },
    ]


@pytest.fixture()
def example_refrigerator_update_response():
    return [
        {"id": 2, "name": "Carrot", "amount": 10},
        {"id": 1, "name": "Bread", "amount": 1},
    ]
