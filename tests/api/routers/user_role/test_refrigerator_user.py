import pytest

from api.routers.user_role.refrigerator_user import (
    get_all_relations_refrigerator,
    create_relation_refrigerator,
    get_relation_refrigerator,
    delete_relation_refrigerator,
)
from api.schemas.refrigerator import (
    RefrigeratorCreate,
    RefrigeratorResponse,
    RefrigeratorCreateResponse,
    RefrigeratorDelete,
)
from api.schemas.user import User


@pytest.mark.asyncio
async def test_get_all_relations_refrigerator(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_users_response,
    example_refrigerator_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_all_relations_refrigerator(requesting_user)

    assert response == example_refrigerator_name_response

    for item in response:
        parsed = RefrigeratorResponse(**item)

        assert isinstance(parsed, RefrigeratorResponse)


@pytest.mark.asyncio
async def test_create_relation_refrigerator(
    mock_supabase_connection,
    example_users_injection,
    example_ingredients_injection,
    example_refrigerator_create,
    example_users_response,
    example_refrigerator_create_response,
):
    requesting_user = User(**example_users_response[0])
    prefered_ingredient = RefrigeratorCreate(**example_refrigerator_create[0])
    response = await create_relation_refrigerator(prefered_ingredient, requesting_user)

    assert response == example_refrigerator_create_response[0]

    parsed = RefrigeratorCreateResponse(**response)

    assert isinstance(parsed, RefrigeratorCreateResponse)


@pytest.mark.asyncio
async def test_get_relation_refrigerator(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_users_response,
    example_refrigerator_name_response,
):
    requesting_user = User(**example_users_response[0])
    response = await get_relation_refrigerator(2, requesting_user)

    assert response == example_refrigerator_name_response[0]

    parsed = RefrigeratorResponse(**response)

    assert isinstance(parsed, RefrigeratorResponse)


@pytest.mark.asyncio
async def test_delete_relation_refrigerator(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_users_response,
    example_refrigerator_response,
):
    requesting_user = User(**example_users_response[0])
    response = await delete_relation_refrigerator(2, requesting_user)

    assert response == example_refrigerator_response[0]

    parsed = RefrigeratorDelete(**response)

    assert isinstance(parsed, RefrigeratorDelete)
