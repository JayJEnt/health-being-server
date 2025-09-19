import pytest

from api.routers.user_role.prefered_ingredients_user import (
    get_all_relations_prefered_ingredients,
    create_relation_prefered_ingredients,
    get_relation_prefered_ingredients,
    delete_relation_prefered_ingredients,
)
from api.schemas.prefered_ingredients import (
    PreferedIngredientsCreate,
    PreferedIngredientsDelete,
    PreferedIngredientsResponse,
    PreferedIngredientsCreateResponse,
)
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_all_relations_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_all_relations_prefered_ingredients(requesting_user)

    assert response == example_prefered_ingredients_name_response

    for item in response:
        parsed = PreferedIngredientsResponse(**item)

        assert isinstance(parsed, PreferedIngredientsResponse)


@pytest.mark.asyncio
async def test_create_relation_prefered_ingredients(
    mock_supabase_connection,
    example_users_injection,
    example_ingredients_injection,
    example_prefered_ingredients_create,
    example_users_response,
    example_prefered_ingredients_create_response,
):
    requesting_user = User(**example_users_response[0])
    prefered_ingredient = PreferedIngredientsCreate(
        **example_prefered_ingredients_create[0]
    )
    response = await create_relation_prefered_ingredients(
        prefered_ingredient, requesting_user
    )

    assert response == example_prefered_ingredients_create_response[0]

    parsed = PreferedIngredientsCreateResponse(**response)

    assert isinstance(parsed, PreferedIngredientsCreateResponse)


@pytest.mark.asyncio
async def test_get_relation_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_prefered_ingredients(2, requesting_user)

    assert response == example_prefered_ingredients_name_response[0]

    parsed = PreferedIngredientsResponse(**response)

    assert isinstance(parsed, PreferedIngredientsResponse)


@pytest.mark.asyncio
async def test_delete_relation_prefered_ingredients(
    mock_supabase_connection,
    example_prefered_ingredients_injection,
    example_users_response,
    example_prefered_ingredients_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_relation_prefered_ingredients(2, requesting_user)

    assert response == example_prefered_ingredients_response[0]

    parsed = PreferedIngredientsDelete(**response)

    assert isinstance(parsed, PreferedIngredientsDelete)
