import pytest

from api.routers.prefered_ingredients import (
    get_all_relations_prefered_ingredients,
    create_relation_prefered_ingredients,
    get_relation_prefered_ingredients,
    delete_relation_prefered_ingredients,
)
from api.schemas.relation.prefered_ingredients import (
    PreferedIngredients,
    CreatePreferedIngredients,
    PostCreatePreferedIngredients,
)
from api.schemas.user import UserResponse


@pytest.mark.asyncio
async def test_get_all_relations_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_name_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await get_all_relations_prefered_ingredients(requesting_user)

    assert response == example_prefered_ingredients_name_response

    # for item in response:
    #     parsed = PreferedIngredients(**item)

    #     assert isinstance(parsed, PreferedIngredients)


@pytest.mark.asyncio
async def test_create_relation_prefered_ingredients(
    mock_supabase_connection,
    example_users_injection,
    example_ingredients_injection,
    example_prefered_ingredients_create,
    example_users_response,
    example_prefered_ingredients_create_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    prefered_ingredient = CreatePreferedIngredients(
        **example_prefered_ingredients_create[0]
    )
    response = await create_relation_prefered_ingredients(
        prefered_ingredient, requesting_user
    )

    assert response == example_prefered_ingredients_create_response[0]

    parsed = PostCreatePreferedIngredients(**response)

    assert isinstance(parsed, PostCreatePreferedIngredients)


@pytest.mark.asyncio
async def test_get_relation_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_name_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await get_relation_prefered_ingredients(2, requesting_user)

    assert response == example_prefered_ingredients_name_response[0]

    # parsed = PreferedIngredientsGet(**response)

    # assert isinstance(parsed, PreferedIngredientsGet)


@pytest.mark.asyncio
async def test_delete_relation_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await delete_relation_prefered_ingredients(2, requesting_user)

    assert response == example_prefered_ingredients_response[0]

    parsed = PreferedIngredients(**response)

    assert isinstance(parsed, PreferedIngredients)
