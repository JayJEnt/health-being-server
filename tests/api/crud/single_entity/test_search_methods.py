import pytest

from api.crud.single_entity.search_methods import search_elements
from api.handlers.http_exceptions import ResourceNotFound


@pytest.mark.asyncio
async def test_search_elements(
    mock_supabase_connection, example_recipes_injection, example_recipes_response
):
    response = await search_elements("recipes", "HealThy")

    assert response == example_recipes_response


@pytest.mark.asyncio
async def test_search_elements_restricted(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_overview_response,
):
    response = await search_elements("recipes", "HealThy", restrict=True)

    assert response == example_recipes_overview_response


@pytest.mark.asyncio
async def test_update_nonexistent_element(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await search_elements("recipes", "Nonexistent")
