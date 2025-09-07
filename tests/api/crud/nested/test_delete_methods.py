import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.nested.post_methods import create_nested
from api.crud.nested.delete_methods import delete_nested
from api.crud.nested.get_methods import get_nested


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


@pytest.mark.asyncio
async def test_delete_nested_elements(mock_supabase_connection):
    await create_element("ingredients", ingredient_create)
    await create_nested("ingredients", 1, ingredient_data_create)
    await delete_nested("ingredients", 1, ["ingredients_data"])
    response = await get_nested("ingredients", 1, ["ingredients_data"])

    assert response == [{"ingredients_data": []}]


@pytest.mark.asyncio
async def test_delete_nested_elements_error(mock_supabase_connection):
    await delete_nested("ingredients", 999, ["ingredients_data"])

    assert True  # No error raised (works as expected)
