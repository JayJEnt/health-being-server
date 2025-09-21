import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.many_entities.post_methods import create_all
from api.handlers.http_exceptions import ResourceNotFound


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
async def test_post_all_elements(mock_supabase_connection):
    await create_element("diet_type", diet_type_create)
    await create_element("ingredients", ingredient_create)
    response = await create_all(
        "recipes", recipe_create_all, related_attributes=["ingredients", "diet_type"]
    )

    assert response == recipe_response


@pytest.mark.asyncio
async def test_post_all_elements_error_resource_not_found(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await create_all(
            "recipes",
            recipe_create_all,
            related_attributes=["ingredients", "diet_type"],
        )
