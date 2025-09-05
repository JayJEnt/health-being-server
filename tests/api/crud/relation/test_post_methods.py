import pytest


from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationship, create_relationships


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


@pytest.mark.asyncio
async def test_create_relationship(mocked_supabase_connection_init):
    await create_element("ingredients", ingredient_create)
    response = await create_relationship("user", 1, "refrigerator", refrigerator_create)

    assert response == {'id': 1, 'name': 'Carrot', 'amount': 50}


@pytest.mark.asyncio
async def test_create_relationships(mocked_supabase_connection_init):
    await create_element("ingredients", ingredient_create)
    response = await create_relationships("user", 1, related_create)

    assert response == [{'refrigerator': [{'id': 1, 'name': 'Carrot', 'amount': 50}]}]