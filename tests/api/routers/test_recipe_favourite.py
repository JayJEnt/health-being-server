import pytest

from api.routers.recipe_favourite import (
    get_all_relations_recipe_favourite,
    create_relation_recipe_favourite,
    get_relation_recipe_favourite,
    delete_relation_recipe_favourite,
)
from api.schemas.recipe_favourite import (
    RecipeFavourite,
    CreateRecipeFavourite,
    PostCreateRecipeFavourite,
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

    # for item in response:
    #     parsed = RecipeFavourite(**item)

    #     assert isinstance(parsed, RecipeFavourite)


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
    prefered_ingredient = CreateRecipeFavourite(**example_recipe_favourite_create[0])
    response = await create_relation_recipe_favourite(
        prefered_ingredient, requesting_user
    )

    assert response == example_recipe_favourite_create_response[0]

    parsed = PostCreateRecipeFavourite(**response)

    assert isinstance(parsed, PostCreateRecipeFavourite)


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

    # parsed = RecipeFavouriteGet(**response)

    # assert isinstance(parsed, RecipeFavouriteGet)


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

    parsed = RecipeFavourite(**response)

    assert isinstance(parsed, RecipeFavourite)
