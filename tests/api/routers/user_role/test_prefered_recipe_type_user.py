import pytest

from api.routers.user_role.prefered_recipe_type_user import (
    create_relation_prefered_recipe_type,
    get_relation_prefered_recipe_type,
    delete_relation_prefered_recipe_type,
)
from api.schemas.prefered_recipe_type import (
    PreferedRecipeTypeCreate,
    PreferedRecipeTypeResponse,
    PreferedRecipeTypeDelete,
)
from api.schemas.diet_type import DietTypeResponse
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_all_relations_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_prefered_recipe_type(requesting_user=requesting_user)

    assert response == example_prefered_recipe_type_name_response

    for item in response:
        parsed = PreferedRecipeTypeResponse(**item)

        assert isinstance(parsed, PreferedRecipeTypeResponse)


@pytest.mark.asyncio
async def test_create_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_users_injection,
    example_diet_types_injection,
    example_prefered_recipe_type_create,
    example_users_response,
    example_prefered_recipe_type_create_response,
):
    requesting_user = User(**example_users_response[0])
    diet_type = PreferedRecipeTypeCreate(**example_prefered_recipe_type_create[0])
    response = await create_relation_prefered_recipe_type(
        diet_type=diet_type, requesting_user=requesting_user
    )

    assert response == example_prefered_recipe_type_create_response[0]

    parsed = DietTypeResponse(**response)

    assert isinstance(parsed, DietTypeResponse)


@pytest.mark.asyncio
async def test_get_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_prefered_recipe_type(
        diet_type_id=1, requesting_user=requesting_user
    )

    assert response == example_prefered_recipe_type_name_response[0]

    parsed = PreferedRecipeTypeResponse(**response)

    assert isinstance(parsed, PreferedRecipeTypeResponse)


@pytest.mark.asyncio
async def test_delete_relation_prefered_recipe_type(
    mock_supabase_connection,
    example_prefered_recipe_type_injection,
    example_users_response,
    example_prefered_recipe_type_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_relation_prefered_recipe_type(
        diet_type_id=1, requesting_user=requesting_user
    )

    assert response == example_prefered_recipe_type_response[0]

    parsed = PreferedRecipeTypeDelete(**response)

    assert isinstance(parsed, PreferedRecipeTypeDelete)
