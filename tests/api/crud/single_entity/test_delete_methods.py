import pytest

from api.crud.single_entity.delete_methods import delete_element_by_id


@pytest.mark.asyncio
async def test_delete_element(
    mock_supabase_connection, example_recipes_injection, example_recipes_response
):
    response = await delete_element_by_id("recipes", 1)

    assert response == example_recipes_response[0]


@pytest.mark.asyncio
async def test_delete_nonexistent_element(mock_supabase_connection):
    with pytest.raises(Exception) as excinfo:
        await delete_element_by_id("recipes", 999)

    assert str(excinfo.value) == "404: Requested resource not found"
