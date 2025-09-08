import pytest

from api.routers.recipes import (
    get_recipes,
    get_recipe,
    search_recipes,
    create_recipe,
    update_recipe,
    delete_recipe,
)
from api.schemas.recipe import RecipeResponse, RecipeOverview
from api.schemas.user import User


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
async def test_get_recipe(
    mock_supabase_connection,
    example_recipes_injection_all,
    example_recipes_response_all,
):
    response = await get_recipe(1)

    assert response == example_recipes_response_all

    parsed = RecipeResponse(**response)

    assert isinstance(parsed, RecipeResponse)


@pytest.mark.asyncio
async def test_search_recipes(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_overview_response,
):
    response = await search_recipes("Healthy Salad")

    assert response == example_recipes_overview_response

    assert isinstance(response, list)

    for item in response:
        parsed = RecipeOverview(**item)

        assert isinstance(parsed, RecipeOverview)


@pytest.mark.asyncio
async def test_create_recipe(
    mock_supabase_connection,
    example_ingredients_injection,
    example_recipes_injection_all,
    example_users_response,
    example_recipes_create_all,
    example_recipes_response_create_all,
):
    requesting_user = User(**example_users_response[0])
    response = await create_recipe(example_recipes_create_all[0], requesting_user)

    assert response == example_recipes_response_create_all

    parsed = RecipeResponse(**response)

    assert isinstance(parsed, RecipeResponse)


@pytest.mark.asyncio
async def test_update_recipe(
    mock_supabase_connection,
    example_diet_types_injection,
    example_ingredients_injection,
    example_recipes_injection_all,
    example_users_response,
    example_recipes_update_all,
    example_recipes_response_update_all,
):
    requesting_user = User(**example_users_response[0])
    response = await update_recipe(1, example_recipes_update_all[0], requesting_user)

    assert response == example_recipes_response_update_all

    parsed = RecipeResponse(**response)

    assert isinstance(parsed, RecipeResponse)


@pytest.mark.asyncio
async def test_delete_recipe(
    mock_supabase_connection,
    example_diet_types_injection,
    example_ingredients_injection,
    example_recipes_injection_all,
    example_users_response,
    example_recipes_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_recipe(1, requesting_user)

    assert response == example_recipes_response[0]
