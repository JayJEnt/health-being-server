import pytest
import pytest_asyncio

from api.crud.many_entities.post_methods import create_all
from api.crud.single_entity.post_methods import create_element


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


@pytest.fixture()
def example_ingredients_create_all(
    example_ingredients_create, example_ingredients_data_create, example_vitamins_create
):
    for index in range(len(example_ingredients_create)):
        example_ingredients_create[index]["ingredients_data"] = (
            example_ingredients_data_create[index // 2]
        )
        example_ingredients_create[index]["vitamins"] = [
            example_vitamins_create[index // 2]
        ]
    return example_ingredients_create


@pytest_asyncio.fixture
async def example_ingredients_injectio_all(
    mock_supabase_connection, example_ingredients_create_all
):
    for ingredient in example_ingredients_create_all:
        await create_all(
            "ingredients",
            ingredient,
            related_attributes=["vitamins"],
            nested_attributes=["ingredients_data"],
        )


@pytest.fixture()
def example_ingredients_response_all():
    return {
        "calories_per_100": 41.6,
        "carbon_per_100": 9.6,
        "fat_per_100": 21.2,
        "fiber_per_100": 2.8,
        "id": 1,
        "ingredient_id": 1,  # TODO: Try to remove duplicated id for nested tables while creating
        "name": "Bread",
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
        "ingredients_data": {
            "ingredient_id": 1,
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
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
def example_ingredients_update_all(
    example_ingredients_update, example_ingredients_data_create, example_vitamins_create
):
    for index in range(len(example_ingredients_update)):
        example_ingredients_update[index]["ingredients_data"] = (
            example_ingredients_data_create[index // 2]
        )
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
        "ingredients_data": {
            "ingredient_id": 1,
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
    }
