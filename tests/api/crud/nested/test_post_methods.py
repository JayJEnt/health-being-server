import pytest

from api.crud.nested.post_methods import create_nested


@pytest.mark.asyncio
async def test_post_nested_elements(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_data_create,
    example_ingredients_data_nested_create_response,
):
    response = await create_nested(
        "ingredients", 1, [{"ingredients_data": example_ingredients_data_create[0]}]
    )
    assert response == [example_ingredients_data_nested_create_response[0]]
