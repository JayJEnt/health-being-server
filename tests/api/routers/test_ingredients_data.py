import pytest

from api.routers.admin_role.ingredients_data import (
    get_ingredient_data,
    create_ingredient_data,
    update_ingredient_data,
    delete_ingredient_data,
)
from api.schemas.ingredient import IngredientDataCreate, IngredientData


@pytest.mark.asyncio
async def test_get_ingredient_data(
    mock_supabase_connection,
    example_ingredients_data_injection,
    example_ingredients_data_response,
):
    response = await get_ingredient_data(ingredient_id=1)

    assert response == example_ingredients_data_response

    parsed = IngredientData(**response)

    assert isinstance(parsed, IngredientData)


@pytest.mark.asyncio
async def test_create_ingredient_data(
    mock_supabase_connection,
    example_ingredients_data_create,
    example_ingredients_data_response,
):
    ingredient_data = IngredientDataCreate(**example_ingredients_data_create[0])
    response = await create_ingredient_data(ingredient=ingredient_data, ingredient_id=1)

    assert response == example_ingredients_data_response

    parsed = IngredientData(**response)

    assert isinstance(parsed, IngredientData)


@pytest.mark.asyncio
async def test_update_ingredient_data(
    mock_supabase_connection,
    example_ingredients_data_injection,
    example_ingredients_data_update,
    example_ingredients_data_update_response,
):
    ingredient_data = IngredientDataCreate(**example_ingredients_data_update[0])
    response = await update_ingredient_data(ingredient=ingredient_data, ingredient_id=1)

    assert response == example_ingredients_data_update_response

    parsed = IngredientData(**response)

    assert isinstance(parsed, IngredientData)


@pytest.mark.asyncio
async def test_delete_ingredient_data(
    mock_supabase_connection,
    example_ingredients_data_injection,
    example_ingredients_data_response,
):
    response = await delete_ingredient_data(ingredient_id=1)

    assert response == example_ingredients_data_response

    parsed = IngredientData(**response)

    assert isinstance(parsed, IngredientData)
