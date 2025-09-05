import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.search_methods import search_elements


recipe_create = {
    "title": "Healthy Salad",
    "description": "A fresh and nutritious salad.",
    "instructions": ["Mix all ingredients in a bowl and serve fresh."],
    "owner_id": 1
}

recipe_response = {
    "id": 1,
    "owner_id": 1,
    "title": "Healthy Salad",
    "description": "A fresh and nutritious salad.",
    "instructions": ["Mix all ingredients in a bowl and serve fresh."],
}

recipe_restricted_response = {
    "id": 1,
    "owner_id": 1,
    "title": "Healthy Salad",
}


@pytest.mark.asyncio
async def test_search_elements(mocked_supabase_connection_init):
    await create_element("recipes", recipe_create)
    response = await search_elements("recipes", "HealThy")

    assert response == [recipe_response]


@pytest.mark.asyncio
async def test_search_elements_restricted(mocked_supabase_connection_init):
    await create_element("recipes", recipe_create)
    response = await search_elements("recipes", "HealThy", restrict=True)

    assert response == [recipe_restricted_response]


@pytest.mark.asyncio
async def test_update_nonexistent_element(mocked_supabase_connection_init):
    with pytest.raises(Exception) as e_info:
        await search_elements("recipes", "Nonexistent")

    assert str(e_info.value) == "404: Requested resource not found"