import pytest


from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationship, create_relationships
from api.crud.relation.get_methods import get_relationship, get_relationships


# TODO: move it to fixtures
ingredient_create = {
    "name": "Carrot",
}

refrigerator_create = {
    "name": "Carrot",
    "amount": 50,
}

related_create = [
    {"refrigerator": [refrigerator_create]},
]


relation_response = {
    'amount': 50.0,
    'ingredient_id': 1,
    'user_id': 1
}

@pytest.mark.asyncio
async def test_get_relationship(mocked_supabase_connection_init):
    await create_element("ingredients", ingredient_create)
    await create_relationship("user", 1, "refrigerator", refrigerator_create)
    response = await get_relationship("user", 1, "refrigerator", 1)

    assert response == relation_response


@pytest.mark.asyncio
async def test_get_relationships(mocked_supabase_connection_init):
    await create_element("ingredients", ingredient_create)
    await create_relationships("user", 1, related_create)
    response = await get_relationships("user", 1, "refrigerator")

    assert response == [relation_response]