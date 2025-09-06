import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.nested.post_methods import create_nested
from api.crud.nested.put_methods import update_nested


ingredient_create = {
    "name": "Carrot",
}

ingredient_data_create = [
    {
        "ingredients_data": {
            "calories_per_100": 41.6,
            "protein_per_100": 0.9,
            "fat_per_100": 21.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        }
    }
]

ingredient_data_update = [
    {
        "ingredients_data": {
            "calories_per_100": 0.6,
            "protein_per_100": 0.9,
            "fat_per_100": 1.2,
            "carbon_per_100": 9.6,
            "fiber_per_100": 2.8,
            "sugar_per_100": 6.8,
            "salt_per_100": 0.1,
        }
    }
]


@pytest.mark.asyncio
async def test_put_nested_elements(mocked_supabase_connection):
    await create_element("ingredients", ingredient_create)
    await create_nested("ingredients", 1, ingredient_data_create)
    response = await update_nested("ingredients", 1, ingredient_data_update)

    assert response == ingredient_data_update


@pytest.mark.asyncio
async def test_put_nested_elements_error(mocked_supabase_connection):
    response = await update_nested("ingredients", 999, ingredient_data_update)

    assert response == []
