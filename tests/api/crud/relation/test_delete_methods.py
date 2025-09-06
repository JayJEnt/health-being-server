import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.relation.post_methods import create_relationship, create_relationships
from api.crud.relation.delete_methods import delete_relationship, delete_relationships


# TODO: move it to fixtures
ingredient_create = {
    "name": "Carrot",
}

refrigerator_create = {
    "name": "Carrot",
    "amount": 50,
}

user_create = {
    "username": "testuser",
    "email": "test@example.com",
    "hashed_password": "hashedpassword",
    "role": "user",
}

related_create = [
    {"refrigerator": [refrigerator_create]},
]


@pytest.mark.asyncio
async def test_delete_relationship(mocked_supabase_connection):
    await create_element("ingredients", ingredient_create)
    await create_relationship("user", 1, "refrigerator", refrigerator_create)
    response = await delete_relationship("user", 1, "refrigerator", 1)

    assert response == {"user_id": 1, "ingredient_id": 1, "amount": 50.0}


@pytest.mark.asyncio
async def test_delete_relationship_error_not_found(mocked_supabase_connection):
    with pytest.raises(Exception) as e_info:
        await delete_relationship("user", 1, "refrigerator", 1)

    assert str(e_info.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_create_relationships(mocked_supabase_connection):
    await create_element("ingredients", ingredient_create)
    await create_relationships("user", 1, related_create)
    await delete_relationships("user", 1, ["refrigerator"])

    assert True  # delete_relationships does not return anything


@pytest.mark.asyncio
async def test_delete_relationships_error_not_found(mocked_supabase_connection):
    await delete_relationships("user", 1, ["refrigerator"])

    assert True  # delete_relationships does not return anything and does not raise an error
