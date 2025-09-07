import pytest

from api.routers.ingredients import (
    get_ingredients,
    get_ingredient,
    get_ingredient_by_name,
    create_ingredient,
    update_ingredient,
    delete_ingredient,
)
from api.schemas.ingredient import Ingredient, IngredientResponse


@pytest.mark.asyncio
async def test_get_ingredients(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_response,
):
    response = await get_ingredients()

    assert response == example_ingredients_response
    assert isinstance(response, list)

    for item in response:
        parsed = Ingredient(**item)

        assert isinstance(parsed, Ingredient)


@pytest.mark.asyncio
async def test_get_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injectio_all,
    example_ingredients_response_all,
):
    response = await get_ingredient(1)

    assert response == example_ingredients_response_all

    parsed = Ingredient(**response)

    assert isinstance(parsed, Ingredient)


@pytest.mark.asyncio
async def test_get_ingredient_by_name(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_response,
):
    response = await get_ingredient_by_name("MusHRoom")

    assert response == example_ingredients_response[2]

    parsed = Ingredient(**response)

    assert isinstance(parsed, Ingredient)


@pytest.mark.asyncio
async def test_create_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_create_all,
    example_ingredients_response_create_all,
):
    response = await create_ingredient(example_ingredients_create_all[0])

    assert response == example_ingredients_response_create_all

    parsed = IngredientResponse(**response)

    assert isinstance(parsed, IngredientResponse)


@pytest.mark.asyncio
async def test_update_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injectio_all,
    example_ingredients_update_all,
    example_ingredients_response_update_all,
):
    response = await update_ingredient(1, example_ingredients_update_all[0])

    assert response == example_ingredients_response_update_all

    parsed = IngredientResponse(**response)

    assert isinstance(parsed, IngredientResponse)


@pytest.mark.asyncio
async def test_delete_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injectio_all,
    example_ingredients_response,
):
    response = await delete_ingredient(1)

    assert response == example_ingredients_response[0]

    parsed = Ingredient(**response)

    assert isinstance(parsed, Ingredient)
