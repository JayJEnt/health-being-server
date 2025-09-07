import pytest
import pytest_asyncio


@pytest.fixture()
def example_ingredients_data_create():
    return [
        {
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "calories_per_100": 14.2,
            "protein_per_100": 4.3,
            "fat_per_100": 11.4,
            "carbon_per_100": 1.6,
            "fiber_per_100": 3.0,
            "sugar_per_100": 1.2,
            "salt_per_100": 0.5,
        },
    ]


@pytest_asyncio.fixture
async def example_ingredients_data_injection(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_data_create,
):
    from api.crud.nested.post_methods import create_nested

    for index in range(len(example_ingredients_data_create)):
        await create_nested(
            "ingredients",
            index + 1,
            [{"ingredients_data": example_ingredients_data_create[index]}],
        )


@pytest.fixture()
def example_ingredients_data_response():
    return [
        {"ingredient_id": 1},
        {"calories_per_100": 41.6},
        {"protein_per_100": 0.9},
        {"fat_per_100": 21.2},
        {"carbon_per_100": 9.6},
        {"fiber_per_100": 2.8},
        {"sugar_per_100": 6.8},
        {"salt_per_100": 0.1},
    ]


@pytest.fixture()
def example_ingredients_data_create_response(example_ingredients_data_create):
    return [
        {"ingredients_data": ingredients_data}
        for ingredients_data in example_ingredients_data_create
    ]


@pytest.fixture()
def example_ingredients_data_update():
    return [
        {
            "calories_per_100": 0.6,
            "protein_per_100": 0.9,
            "fat_per_100": 1.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        },
        {
            "calories_per_100": 1.2,
            "protein_per_100": 4.7,
            "fat_per_100": 1.3,
            "carbon_per_100": 1.6,
            "fiber_per_100": 3.4,
            "sugar_per_100": 1.2,
            "salt_per_100": 0.5,
        },
    ]


@pytest.fixture()
def example_ingredients_data_update_response(example_ingredients_data_update):
    return [
        {"ingredients_data": ingredients_data}
        for ingredients_data in example_ingredients_data_update
    ]
