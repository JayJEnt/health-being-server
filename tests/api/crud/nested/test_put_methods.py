import pytest

from api.crud.nested.put_methods import update_nested


@pytest.mark.asyncio
async def test_put_nested_elements(
    mock_supabase_connection,
    example_ingredients_data_injection,
    example_ingredients_data_update,
    example_ingredients_data_update_response,
):
    response = await update_nested(
        "ingredients", 1, [{"ingredients_data": example_ingredients_data_update[0]}]
    )

    assert response == [example_ingredients_data_update_response[0]]


@pytest.mark.asyncio
async def test_put_nested_elements_error(
    mock_supabase_connection, example_ingredients_data_update
):
    response = await update_nested(
        "ingredients", 999, [{"ingredients_data": example_ingredients_data_update[0]}]
    )

    assert response == []
