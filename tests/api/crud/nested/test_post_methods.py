import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.nested.post_methods import create_nested


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
async def test_post_nested_elements(mock_supabase_connection):
    await create_element("ingredients", ingredient_create)
    response = await create_nested("ingredients", 1, ingredient_data_create)
    assert response == ingredient_data_create
