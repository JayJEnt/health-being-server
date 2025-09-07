import pytest

from api.crud.nested.delete_methods import delete_nested
from api.crud.nested.get_methods import get_nested


@pytest.mark.asyncio
async def test_delete_nested_elements(
    mock_supabase_connection, example_ingredients_data_injection
):
    await delete_nested("ingredients", 1, ["ingredients_data"])
    response = await get_nested("ingredients", 1, ["ingredients_data"])

    assert response == [{"ingredients_data": []}]


@pytest.mark.asyncio
async def test_delete_nested_elements_error(mock_supabase_connection):
    await delete_nested("ingredients", 999, ["ingredients_data"])

    assert True  # No error raised (works as expected)
