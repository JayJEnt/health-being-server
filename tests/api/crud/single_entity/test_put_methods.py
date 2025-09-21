import pytest

from api.crud.single_entity.put_methods import update_element_by_id
from api.handlers.http_exceptions import ResourceNotFound


@pytest.mark.asyncio
async def test_update_element(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_update,
    example_recipes_updated_response,
):
    response = await update_element_by_id("recipes", 1, example_recipes_update[0])

    assert response == example_recipes_updated_response[0]


@pytest.mark.asyncio
async def test_update_nonexistent_element(
    mock_supabase_connection, example_recipes_update
):
    with pytest.raises(ResourceNotFound):
        await update_element_by_id("recipes", 999, example_recipes_update[0])
