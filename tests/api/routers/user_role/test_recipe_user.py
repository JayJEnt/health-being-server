import pytest

from api.routers.user_role.recipes_user import (
    create_recipe,
    update_recipe,
    delete_recipe,
)
from api.schemas.recipe import RecipeResponse, Recipe
from api.schemas.user import User


@pytest.mark.asyncio
async def test_create_recipe(
    mock_supabase_connection,
    example_ingredients_injection,
    example_diet_types_injection,
    example_users_response,
    example_recipes_create_all,
    example_recipes_response_create_all,
):
    requesting_user = User(**example_users_response[0])
    response = await create_recipe(
        recipe=example_recipes_create_all[0], requesting_user=requesting_user
    )

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
    response = await update_recipe(
        recipe=example_recipes_update_all[0],
        recipe_id=1,
        requesting_user=requesting_user,
    )

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
    response = await delete_recipe(recipe_id=1, requesting_user=requesting_user)

    assert response == example_recipes_response[0]

    parsed = Recipe(**response)

    assert isinstance(parsed, Recipe)
