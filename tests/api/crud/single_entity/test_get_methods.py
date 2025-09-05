import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.get_methods import get_elements, get_element_by_name, get_element_by_id


# TODO: move to fixture file
user_create = {
        "username": "New User",
        "email": "newuser@example.com",
        "hashed_password": "securepassword123",
        "role": "user",
    }


user_response = {
    'id': 1,
    'username': 'New User',
    'email': 'newuser@example.com',
    'hashed_password': 'securepassword123',
    'role': 'user'
}

recipe_create = {
    "title": "Healthy Salad",
    "description": "A fresh and nutritious salad.",
    "instructions": ["Mix all ingredients in a bowl and serve fresh."],
    "owner_id": 1
}


recipe_restricted_response = {
    "id": 1,
    "owner_id": 1,
    "title": "Healthy Salad",
}


@pytest.mark.asyncio
async def test_get_elements(mocked_supabase_connection_init):
    await create_element("user", user_create)
    response = await get_elements("user")

    assert response == [user_response]


@pytest.mark.asyncio
async def test_get_elements_restricted(mocked_supabase_connection_init):
    await create_element("recipes", recipe_create)
    response = await get_elements("recipes", restrict=True)

    assert response == [recipe_restricted_response]


@pytest.mark.asyncio
async def test_get_element_by_name(mocked_supabase_connection_init):
    await create_element("user", user_create)
    response = await get_element_by_name("user", "New User")

    assert response == user_response


@pytest.mark.asyncio
async def test_get_element_by_alternative_name(mocked_supabase_connection_init):
    await create_element("user", user_create)
    response = await get_element_by_name("user", "newuser@example.com", alternative_name=True)

    assert response == user_response


@pytest.mark.asyncio
async def test_get_element_by_name_error(mocked_supabase_connection_init):
    with pytest.raises(Exception) as excinfo:
        await get_element_by_name("user", "New User")

    assert  str(excinfo.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_get_element_by_id(mocked_supabase_connection_init):
    await create_element("user", user_create)
    response = await get_element_by_id("user", 1)

    assert response == user_response


@pytest.mark.asyncio
async def test_get_element_by_id_error(mocked_supabase_connection_init):
    with pytest.raises(Exception) as excinfo:
        await get_element_by_id("user", 999)

    assert  str(excinfo.value) == "404: Requested resource not found"
