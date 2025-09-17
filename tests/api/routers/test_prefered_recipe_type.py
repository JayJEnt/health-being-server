import pytest

from api.routers.prefered_recipe_type import (
    get_all_relations_prefered_recipe_type,
    create_relation_prefered_recipe_type,
    get_relation_prefered_recipe_type,
    delete_relation_prefered_recipe_type,
)
from api.schemas.relation.prefered_recipe_type import (
    PreferedRecipeType,
    CreatePreferedRecipeType,
    PostCreatePreferedRecipeType,
)
from api.schemas.user import UserResponse


@pytest.mark.asyncio
async def test_get_all_relations_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_name_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await get_all_relations_prefered_recipe_type(requesting_user)

    assert response == example_prefered_recipe_type_name_response

    # for item in response:
    #     parsed = PreferedRecipeType(**item)

    #     assert isinstance(parsed, PreferedRecipeType)


@pytest.mark.asyncio
async def test_create_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_users_injection,
    example_diet_types_injection,
    example_prefered_recipe_type_create,
    example_users_response,
    example_prefered_recipe_type_create_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    prefered_ingredient = CreatePreferedRecipeType(
        **example_prefered_recipe_type_create[0]
    )
    response = await create_relation_prefered_recipe_type(
        prefered_ingredient, requesting_user
    )

    assert response == example_prefered_recipe_type_create_response[0]

    parsed = PostCreatePreferedRecipeType(**response)

    assert isinstance(parsed, PostCreatePreferedRecipeType)


@pytest.mark.asyncio
async def test_get_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_name_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await get_relation_prefered_recipe_type(1, requesting_user)

    assert response == example_prefered_recipe_type_name_response[0]

    # parsed = PreferedRecipeTypeGet(**response)

    # assert isinstance(parsed, PreferedRecipeTypeGet)


@pytest.mark.asyncio
async def test_delete_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_response,
):
    requesting_user = UserResponse(**example_users_response[0])
    response = await delete_relation_prefered_recipe_type(1, requesting_user)

    assert response == example_prefered_recipe_type_response[0]

    parsed = PreferedRecipeType(**response)

    assert isinstance(parsed, PreferedRecipeType)
