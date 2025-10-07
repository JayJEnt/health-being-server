import pytest
import pytest_asyncio

from api.crud.many_entities.post_methods import create_all
from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_ingredients_create():
    return [
        {
            "name": "Bread",
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "name": "Carrot",
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "name": "Mushroom",
        },
        {
            "name": "Rice",
        },
    ]


@pytest_asyncio.fixture
async def example_ingredients_injection(
    mock_supabase_connection, example_ingredients_create
):
    for ingredient in example_ingredients_create:
        await create_element("ingredients", ingredient)


@pytest.fixture()
def example_ingredients_response():
    return [
        {
            "id": 1,
            "name": "Bread",
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "id": 2,
            "name": "Carrot",
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "id": 3,
            "name": "Mushroom",
            "calories_per_100": None,
            "protein_per_100": None,
            "fat_per_100": None,
            "carbon_per_100": None,
            "fiber_per_100": None,
            "sugar_per_100": None,
            "salt_per_100": None,
        },
        {
            "id": 4,
            "name": "Rice",
            "calories_per_100": None,
            "protein_per_100": None,
            "fat_per_100": None,
            "carbon_per_100": None,
            "fiber_per_100": None,
            "sugar_per_100": None,
            "salt_per_100": None,
        },
    ]


@pytest.fixture()
def example_ingredients_create_all(example_ingredients_create, example_vitamins_create):
    for index in range(len(example_ingredients_create)):
        example_ingredients_create[index]["vitamins"] = [
            example_vitamins_create[index // 2]
        ]
    return example_ingredients_create


@pytest_asyncio.fixture
async def example_ingredients_injection_all(
    mock_supabase_connection, example_ingredients_create_all
):
    for ingredient in example_ingredients_create_all:
        await create_all(
            "ingredients",
            ingredient,
            related_attributes=["vitamins"],
        )


@pytest.fixture()
def example_ingredients_response_all():
    return {
        "id": 1,
        "name": "Bread",
        "calories_per_100": 41.6,
        "carbon_per_100": 9.6,
        "fat_per_100": 21.2,
        "fiber_per_100": 2.8,
        "protein_per_100": 0.9,
        "salt_per_100": 0.1,
        "sugar_per_100": 6.8,
        "vitamins": [
            {
                "id": 1,
                "name": "C",
            },
        ],
    }


@pytest.fixture()
def example_ingredients_response_create_all():
    return {
        "id": 1,
        "name": "Bread",
        "vitamins": [{"id": 1, "name": "C"}],
        "calories_per_100": 41.6,
        "protein_per_100": 0.9,
        "fat_per_100": 21.2,
        "carbon_per_100": 9.6,
        "fiber_per_100": 2.8,
        "sugar_per_100": 6.8,
        "salt_per_100": 0.1,
    }


@pytest.fixture()
def example_ingredients_update():
    return [
        {"name": "Raspberry"},
        {"name": "Lemon"},
        {"name": "Mushroom"},
        {"name": "Rice"},
    ]


@pytest.fixture()
def example_ingredients_update_all(example_ingredients_update, example_vitamins_create):
    for index in range(len(example_ingredients_update)):
        example_ingredients_update[index]["vitamins"] = [
            example_vitamins_create[index // 2]
        ]
    return example_ingredients_update


@pytest.fixture()
def example_ingredients_response_update_all():
    return {
        "id": 1,
        "name": "Raspberry",
        "vitamins": [{"id": 1, "name": "C"}],
        "calories_per_100": 41.6,
        "protein_per_100": 0.9,
        "fat_per_100": 21.2,
        "carbon_per_100": 9.6,
        "fiber_per_100": 2.8,
        "sugar_per_100": 6.8,
        "salt_per_100": 0.1,
    }
