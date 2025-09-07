import pytest
import pytest_asyncio


@pytest.fixture()
def example_recipes_create():
    return [
        {
            "title": "Healthy Salad",
            "description": "A fresh and healthy salad.",
            "instructions": ["Mix all ingredients in a bowl and serve fresh."],
            "owner_id": 1,
        }
    ]


@pytest_asyncio.fixture
async def example_recipes_injection(mock_supabase_connection, example_recipes_create):
    from api.crud.single_entity.post_methods import create_element

    for recipe in example_recipes_create:
        await create_element("recipes", recipe)


@pytest.fixture()
def example_recipes_response():
    return [
        {
            "id": 1,
            "title": "Healthy Salad",
            "description": "A fresh and healthy salad.",
            "instructions": ["Mix all ingredients in a bowl and serve fresh."],
            "owner_id": 1,
        }
    ]


@pytest.fixture()
def example_recipes_restricted_response():
    return [
        {
            "id": 1,
            "owner_id": 1,
            "title": "Healthy Salad",
        }
    ]


@pytest.fixture()
def example_recipes_update():
    return [
        {
            "title": "Not Healthy Salad",
            "description": "A fresh and not healthy salad.",
            "instructions": ["Mix all ingredients in a bowl and serve fresh."],
            "owner_id": 1,
        }
    ]


@pytest.fixture()
def example_recipes_updated_response():
    return [
        {
            "id": 1,
            "title": "Not Healthy Salad",
            "description": "A fresh and not healthy salad.",
            "instructions": ["Mix all ingredients in a bowl and serve fresh."],
            "owner_id": 1,
        }
    ]
