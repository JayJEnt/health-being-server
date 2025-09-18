import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_diet_types_create():
    return [
        {
            "diet_name": "vege",
        },
        {
            "diet_name": "vegan",
        },
        {
            "diet_name": "low_carb",
        },
    ]


@pytest_asyncio.fixture
async def example_diet_types_injection(
    mock_supabase_connection, example_diet_types_create
):
    for diet_type in example_diet_types_create:
        await create_element("diet_type", diet_type)


@pytest.fixture()
def example_diet_types_response():
    return [
        {
            "id": 1,
            "diet_name": "vege",
        },
        {
            "id": 2,
            "diet_name": "vegan",
        },
        {
            "id": 3,
            "diet_name": "low_carb",
        },
    ]


@pytest.fixture()
def example_diet_types_update():
    return [
        {
            "diet_name": "vegetarian",
        },
        {
            "diet_name": "vegan",
        },
    ]


@pytest.fixture()
def example_diet_types_update_response():
    return [
        {
            "id": 1,
            "diet_name": "vegetarian",
        },
        {
            "id": 2,
            "diet_name": "vegan",
        },
        {
            "id": 3,
            "diet_name": "low_carb",
        },
    ]
