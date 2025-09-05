import pytest

from api.crud.single_entity.post_methods import create_element


@pytest.mark.asyncio
async def test_create_element(mocked_supabase_connection_init):
    response = await create_element("vitamins", {"name": "New Vitamin"})

    assert response == {'id': 1, 'name': 'New Vitamin'}
