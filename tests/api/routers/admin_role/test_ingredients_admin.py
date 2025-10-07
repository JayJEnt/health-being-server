import pytest

from api.routers.admin_role.ingredients_admin import (
    create_ingredient,
    update_ingredient,
    delete_ingredient,
)
from api.schemas.ingredient import IngredientResponseAll


@pytest.mark.asyncio
async def test_create_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_create_all,
    example_ingredients_response_create_all,
):
    response = await create_ingredient(example_ingredients_create_all[0])

    assert response == example_ingredients_response_create_all

    parsed = IngredientResponseAll(**response)

    assert isinstance(parsed, IngredientResponseAll)


@pytest.mark.asyncio
async def test_update_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injection_all,
    example_ingredients_update_all,
    example_ingredients_response_update_all,
):
    response = await update_ingredient(1, example_ingredients_update_all[0])

    assert response == example_ingredients_response_update_all

    parsed = IngredientResponseAll(**response)

    assert isinstance(parsed, IngredientResponseAll)


@pytest.mark.asyncio
async def test_delete_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injection_all,
    example_ingredients_response,
):
    response = await delete_ingredient(1)

    assert response == example_ingredients_response[0]

    parsed = IngredientResponseAll(**response)

    assert isinstance(parsed, IngredientResponseAll)
