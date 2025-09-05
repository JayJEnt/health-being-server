import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.put_methods import update_element_by_id


@pytest.mark.asyncio
async def test_update_element(mocked_supabase_connection_init):
    await create_element("vitamins", {"name": "New Vitamin"})
    response = await update_element_by_id("vitamins", 1, {"name": "Updated Vitamin"})

    assert response == {'id': 1, 'name': 'Updated Vitamin'}


@pytest.mark.asyncio
async def test_update_nonexistent_element(mocked_supabase_connection_init):
    with pytest.raises(Exception) as excinfo:
        await update_element_by_id("vitamins", 999, {"name": "Nonexistent Vitamin"})

    assert  str(excinfo.value) == "404: Requested resource not found"