import pytest

from api.routers.public.recipes_public import get_recipes
from api.schemas.recipe import RecipeResponseGet, RecipeOverview


@pytest.mark.asyncio
async def test_get_recipes(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_overview_response,
):
    response = await get_recipes()

    assert response == example_recipes_overview_response
    assert isinstance(response, list)

    for item in response:
        parsed = RecipeOverview(**item)

        assert isinstance(parsed, RecipeOverview)


@pytest.mark.asyncio
async def test_search_recipes(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_overview_response,
):
    response = await get_recipes(phrase="Healthy Salad")

    assert response == example_recipes_overview_response

    assert isinstance(response, list)

    for item in response:
        parsed = RecipeOverview(**item)

        assert isinstance(parsed, RecipeOverview)


@pytest.mark.asyncio
async def test_get_recipe(
    mock_supabase_connection,
    example_recipes_injection_all,
    example_recipes_response_all_get,
):
    response = await get_recipes(recipe_id=1)

    assert response == example_recipes_response_all_get

    parsed = RecipeResponseGet(**response)

    assert isinstance(parsed, RecipeResponseGet)
