import pytest

from api.crud.single_entity.post_methods import create_element
from api.crud.single_entity.delete_methods import delete_element_by_id


@pytest.mark.asyncio
async def test_delete_element(mocked_supabase_connection):
    await create_element("vitamins", {"name": "New Vitamin"})
    response = await delete_element_by_id("vitamins", 1)

    assert response == {"id": 1, "name": "New Vitamin"}


@pytest.mark.asyncio
async def test_delete_nonexistent_element(mocked_supabase_connection):
    with pytest.raises(Exception) as excinfo:
        await delete_element_by_id("vitamins", 999)

    assert str(excinfo.value) == "404: Requested resource not found"
