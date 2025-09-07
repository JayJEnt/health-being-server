import pytest

from api.crud.nested.get_methods import get_nested


@pytest.mark.asyncio
async def test_post_nested_elements(
    mock_supabase_connection,
    example_ingredients_data_injection,
    example_ingredients_data_get_response,
):
    response = await get_nested("ingredients", 1, ["ingredients_data"])

    assert response == example_ingredients_data_get_response


@pytest.mark.asyncio
async def test_post_nested_elements_error(mock_supabase_connection):
    response = await get_nested("ingredients", 1, ["ingredients_data"])

    assert response == [{"ingredients_data": []}]
