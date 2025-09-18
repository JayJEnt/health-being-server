import pytest
import pytest_asyncio

from api.crud.many_entities.post_methods import create_all
from api.crud.single_entity.post_methods import create_element


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
def example_recipes_overview_response():
    return [
        {
            "id": 1,
            "title": "Healthy Salad",
            "owner_id": 1,
        }
    ]


@pytest.fixture()
def example_recipes_create_all():
    return [
        {
            "title": "Healthy Salad",
            "description": "A fresh and healthy salad.",
            "instructions": ["Mix all ingredients in a bowl and serve fresh."],
            "diet_type": [{"diet_name": "vege"}],
            "ingredients": [{"name": "Carrot", "amount": 5, "measure_unit": ""}],
            "owner_id": 1,
        }
    ]


@pytest_asyncio.fixture
async def example_recipes_injection_all(
    mock_supabase_connection,
    example_recipes_create_all,
    example_diet_types_injection,
    example_ingredients_injection,
):
    for recipe in example_recipes_create_all:
        await create_all(
            "recipes",
            recipe,
            related_attributes=["ingredients", "diet_type"],
        )


@pytest.fixture()
def example_recipes_response_all():
    return {
        "id": 1,
        "owner_id": 1,
        "title": "Healthy Salad",
        "description": "A fresh and healthy salad.",
        "instructions": ["Mix all ingredients in a bowl and serve fresh."],
        "ingredients": [{"id": 2, "name": "Carrot", "amount": 5.0, "measure_unit": ""}],
        "diet_type": [{"id": 1, "diet_name": "vege"}],
    }


@pytest.fixture()
def example_recipes_response_create_all():
    return {
        "id": 1,
        "owner_id": 1,
        "title": "Healthy Salad",
        "description": "A fresh and healthy salad.",
        "instructions": ["Mix all ingredients in a bowl and serve fresh."],
        "ingredients": [{"id": 2, "name": "Carrot", "amount": 5, "measure_unit": ""}],
        "diet_type": [{"id": 1, "diet_name": "vege"}],
    }


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


@pytest.fixture()
def example_recipes_update_all():
    return [
        {
            "title": "Changed",
            "description": "A fresh and healthy salad.",
            "instructions": ["Also Changed"],
            "diet_type": [{"diet_name": "Vege"}],
            "ingredients": [{"name": "Carrot", "amount": 1, "measure_unit": ""}],
            "owner_id": 1,
        }
    ]


@pytest.fixture()
def example_recipes_response_update_all():
    return {
        "id": 1,
        "owner_id": 1,
        "title": "Changed",
        "description": "A fresh and healthy salad.",
        "instructions": ["Also Changed"],
        "ingredients": [{"id": 2, "name": "Carrot", "amount": 1, "measure_unit": ""}],
        "diet_type": [{"id": 1, "diet_name": "vege"}],
    }
