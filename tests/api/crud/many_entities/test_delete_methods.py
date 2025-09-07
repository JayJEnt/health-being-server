import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.many_entities.post_methods import create_all
from api.crud.many_entities.delete_methods import delete_all
from api.crud.many_entities.get_methods import get_all


diet_type_create = {
    "diet_name": "test diet",
}


ingredient_create = {
    "name": "test ingredient",
}


recipe_create_all = {
    "title": "test",
    "description": "test recipe",
    "instructions": [
        "prepare ingredients",
        "cook ingredients",
    ],
    "diet_type": [
        {
            "diet_name": "test diet",
        }
    ],
    "ingredients": [{"name": "test ingredient", "amount": 5, "measure_unit": "szt."}],
    "owner_id": 1,
}


recipe_response = {
    "id": 1,
    "owner_id": 1,
    "title": "test",
    "description": "test recipe",
    "instructions": ["prepare ingredients", "cook ingredients"],
    "ingredients": [
        {"id": 1, "name": "test ingredient", "amount": 5, "measure_unit": "szt."}
    ],
    "diet_type": [{"id": 1, "diet_name": "test diet"}],
}


recipe_response_resource_not_found = {
    "id": 1,
    "owner_id": 1,
    "title": "test",
    "description": "test recipe",
    "instructions": ["prepare ingredients", "cook ingredients"],
    "ingredients": [None],
    "diet_type": [None],
}


@pytest.mark.asyncio
async def test_delete_all_elements(mock_supabase_connection):
    await create_element("diet_type", diet_type_create)
    await create_element("ingredients", ingredient_create)
    await create_all(
        "recipes", recipe_create_all, related_attributes=["ingredients", "diet_type"]
    )
    await delete_all("recipes", 1, related_attributes=["ingredients", "diet_type"])
    with pytest.raises(Exception) as e_info:
        await get_all("recipes", 1, related_attributes=["ingredients", "diet_type"])

    assert str(e_info.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_delete_all_elements_error_resource_not_found(mock_supabase_connection):
    with pytest.raises(Exception) as e_info:
        await delete_all("recipes", 1, related_attributes=["ingredients", "diet_type"])

    assert str(e_info.value) == "404: Requested resource not found"
