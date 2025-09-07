import pytest
import pytest_asyncio


@pytest.fixture()
def example_vitamins_included_create():
    return [
        {
            "ingredient_id": 1,
            "vitamin_id": 1,
        },
        {
            "ingredient_id": 2,
            "vitamin_id": 2,
        },
    ]


@pytest_asyncio.fixture
async def example_vitamins_included_injection(
    mock_supabase_connection, example_vitamins_included_create
):
    from api.crud.single_entity.post_methods import create_element

    for vitamin in example_vitamins_included_create:
        await create_element("vitamins_included", vitamin)


@pytest.fixture()
def example_vitamins_included_response(example_vitamins_included_create):
    return example_vitamins_included_create
