import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.many_entities.post_methods import create_all
from api.crud.many_entities.put_methods import update_all
from api.handlers.http_exceptions import ResourceNotFound


diet_type_create = {
    "diet_name": "test diet",
}


diet_type_create2 = {
    "diet_name": "test diet 2",
}


ingredient_create = {
    "name": "test ingredient",
}


ingredient_create2 = {
    "name": "test ingredient 2",
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


recipe_update_all = {
    "title": "test updated",
    "description": "test recipe updated",
    "instructions": [
        "prepare ingredients",
        "no more cooking needed",
    ],
    "diet_type": [
        {
            "diet_name": "test diet 2",
        }
    ],
    "ingredients": [{"name": "test ingredient 2", "amount": 1, "measure_unit": "szt."}],
    "owner_id": 1,
}


recipe_response = {
    "id": 1,
    "owner_id": 1,
    "title": "test updated",
    "description": "test recipe updated",
    "instructions": ["prepare ingredients", "no more cooking needed"],
    "ingredients": [
        {"id": 2, "name": "test ingredient 2", "amount": 1, "measure_unit": "szt."}
    ],
    "diet_type": [{"id": 2, "diet_name": "test diet 2"}],
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
async def test_put_all_elements(mock_supabase_connection):
    await create_element("diet_type", diet_type_create)
    await create_element("ingredients", ingredient_create)
    await create_element("diet_type", diet_type_create2)
    await create_element("ingredients", ingredient_create2)
    await create_all(
        "recipes", recipe_create_all, related_attributes=["ingredients", "diet_type"]
    )
    response = await update_all(
        "recipes", 1, recipe_update_all, related_attributes=["ingredients", "diet_type"]
    )

    assert response == recipe_response


@pytest.mark.asyncio
async def test_put_all_elements_error_resource_not_found(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await update_all(
            "recipes",
            1,
            recipe_update_all,
            related_attributes=["ingredients", "diet_type"],
        )
