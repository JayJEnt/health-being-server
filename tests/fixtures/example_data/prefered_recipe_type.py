import pytest
import pytest_asyncio

from api.crud.relation.post_methods import create_relationship


@pytest.fixture()
def example_prefered_recipe_type_create():
    return [
        {
            "diet_name": "vege",
        },
    ]


@pytest_asyncio.fixture
async def example_prefered_recipe_type_injection(
    mock_supabase_connection,
    example_prefered_recipe_type_create,
    example_users_injection,
    example_diet_types_injection,
):
    for diet_type in example_prefered_recipe_type_create:
        await create_relationship("user", 1, "diet_type", diet_type)


@pytest.fixture()
def example_prefered_recipe_type_create_response():
    return [
        {"id": 1, "diet_name": "vege"},
    ]


@pytest.fixture()
def example_prefered_recipe_type_response():
    return [
        {"user_id": 1, "type_id": 1},
    ]


@pytest.fixture()
def example_prefered_recipe_type_name_response():
    return [
        {
            "type_id": 1,
            "diet_name": "vege",
        },
    ]
