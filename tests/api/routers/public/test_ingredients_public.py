import pytest

from api.routers.public.ingredients_public import get_ingredients
from api.schemas.ingredient import IngredientResponse


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
        parsed = IngredientResponse(**item)

        assert isinstance(parsed, IngredientResponse)


@pytest.mark.asyncio
async def test_get_ingredient(
    mock_supabase_connection,
    example_vitamins_injection,
    example_ingredients_injection_all,
    example_ingredients_response,
):
    response = await get_ingredients(ingredient_id=1)

    assert response == example_ingredients_response[0]

    parsed = IngredientResponse(**response)

    assert isinstance(parsed, IngredientResponse)


@pytest.mark.asyncio
async def test_get_ingredient_by_name(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_response,
):
    response = await get_ingredients(ingredient_name="Mushroom")

    assert response == example_ingredients_response[2]

    parsed = IngredientResponse(**response)

    assert isinstance(parsed, IngredientResponse)


@pytest.mark.asyncio
async def test_get_ingredients_by_search_phrase(
    mock_supabase_connection,
    example_ingredients_injection,
    example_ingredients_response,
):

    response = await get_ingredients(phrase="o")

    assert response == [
        example_ingredients_response[1],
        example_ingredients_response[2],
    ]

    for item in response:
        parsed = IngredientResponse(**item)
        assert isinstance(parsed, IngredientResponse)
