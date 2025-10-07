import pytest

from api.crud.many_entities.get_methods import get_all
from api.handlers.http_exceptions import ResourceNotFound


@pytest.mark.asyncio
async def test_get_all_elements(
    mock_supabase_connection,
    example_recipes_injection_all,
    example_recipes_response_all,
):
    response = await get_all(
        "recipes", 1, related_attributes=["ingredients", "diet_type"]
    )

    assert response == example_recipes_response_all


@pytest.mark.asyncio
async def test_get_all_elements_error_resource_not_found(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await get_all("recipes", 1, related_attributes=["ingredients", "diet_type"])
