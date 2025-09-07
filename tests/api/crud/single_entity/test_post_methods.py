import pytest

from api.crud.single_entity.post_methods import create_element


@pytest.mark.asyncio
async def test_create_element(
    mock_supabase_connection, example_recipes_create, example_recipes_response
):
    response = await create_element("recipes", example_recipes_create[0])

    assert response == example_recipes_response[0]
