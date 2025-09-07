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
async def test_create_relationship(mock_supabase_connection):
    await create_element("ingredients", ingredient_create)
    response = await create_relationship("user", 1, "refrigerator", refrigerator_create)

    assert response == {"id": 1, "name": "Carrot", "amount": 50}


@pytest.mark.asyncio
async def test_create_relationship_error_not_found(mock_supabase_connection):
    response = await create_relationship("user", 1, "refrigerator", refrigerator_create)

    assert response is None


@pytest.mark.asyncio
async def test_create_relationship_error_reference_to_itself(
    mock_supabase_connection,
):
    await create_element("user", user_create)
    with pytest.raises(Exception) as e_info:
        await create_relationship("user", 1, "user", user_create)

    assert str(e_info.value) == "405: Referencing to itself is not allowed"


@pytest.mark.asyncio
async def test_create_relationships(mock_supabase_connection):
    await create_element("ingredients", ingredient_create)
    response = await create_relationships("user", 1, related_create)

    assert response == [{"refrigerator": [{"id": 1, "name": "Carrot", "amount": 50}]}]
