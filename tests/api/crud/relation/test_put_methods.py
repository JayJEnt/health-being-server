import pytest


from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationships
from api.crud.relation.put_methods import update_relationships


# TODO: move it to fixtures
ingredient_create = {
    "name": "Carrot",
}

refrigerator_create = {
    "name": "Carrot",
    "amount": 50,
}

ingredient_create2 = {
    "name": "Mushroom",
}

refrigerator_create2 = {
    "name": "Mushroom",
    "amount": 18,
}

related_create = [
    {"refrigerator": [refrigerator_create, refrigerator_create2]},
]

refrigerator_update = {
    "name": "Carrot",
    "amount": 10,
}

refrigerator_update2 = {
    "name": "Mushroom",
    "amount": 9,
}

related_update = [
    {"refrigerator": [refrigerator_update, refrigerator_update2]},
]


@pytest.mark.asyncio
async def test_update_relationships(mock_supabase_connection):
    await create_element("ingredients", ingredient_create)
    await create_element("ingredients", ingredient_create2)
    await create_relationships("user", 1, related_create)
    response = await update_relationships("user", 1, related_update)

    assert response == [
        {
            "refrigerator": [
                {"id": 1, "name": "Carrot", "amount": 10},
                {"id": 2, "name": "Mushroom", "amount": 9},
            ]
        }
    ]


@pytest.mark.asyncio
async def test_update_relationships_error(mock_supabase_connection):
    response = await update_relationships("user", 999, related_update)

    assert response == [{"refrigerator": [None, None]}]
