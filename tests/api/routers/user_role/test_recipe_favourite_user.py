import pytest

from api.routers.user_role.recipe_favourite_user import (
    get_all_relations_recipe_favourite,
    create_relation_recipe_favourite,
    get_relation_recipe_favourite,
    delete_relation_recipe_favourite,
)
from api.schemas.recipe_favourite import (
    RecipeFavouriteDelete,
    RecipeFavouriteCreate,
    RecipeFavouriteCreateResponse,
    RecipeFavouriteResponse,
)
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_all_relations_recipe_favourite(
    mock_supabase_connection,
    example_recipe_favourite_injection,
    example_users_response,
    example_recipe_favourite_names_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_all_relations_recipe_favourite(requesting_user)

    assert response == example_recipe_favourite_names_response

    for item in response:
        parsed = RecipeFavouriteResponse(**item)

        assert isinstance(parsed, RecipeFavouriteResponse)


@pytest.mark.asyncio
async def test_create_relation_recipe_favourite(
    mock_supabase_connection,
    example_users_injection,
    example_recipes_injection,
    example_recipe_favourite_create,
    example_users_response,
    example_recipe_favourite_create_response,
):
    requesting_user = User(**example_users_response[0])
    prefered_ingredient = RecipeFavouriteCreate(**example_recipe_favourite_create[0])
    response = await create_relation_recipe_favourite(
        prefered_ingredient, requesting_user
    )

    assert response == example_recipe_favourite_create_response[0]

    parsed = RecipeFavouriteCreateResponse(**response)

    assert isinstance(parsed, RecipeFavouriteCreateResponse)


@pytest.mark.asyncio
async def test_get_relation_recipe_favourite(
    mock_supabase_connection,
    example_recipe_favourite_injection,
    example_users_response,
    example_recipe_favourite_names_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_recipe_favourite(1, requesting_user)

    assert response == example_recipe_favourite_names_response[0]

    parsed = RecipeFavouriteResponse(**response)

    assert isinstance(parsed, RecipeFavouriteResponse)


@pytest.mark.asyncio
async def test_delete_relation_recipe_favourite(
    mock_supabase_connection,
    example_recipe_favourite_injection,
    example_users_response,
    example_recipe_favourite_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_relation_recipe_favourite(1, requesting_user)

    assert response == example_recipe_favourite_response[0]

    parsed = RecipeFavouriteDelete(**response)

    assert isinstance(parsed, RecipeFavouriteDelete)
