import pytest

from api.routers.admin_role.vitamins_admin import (
    create_vitamin,
    update_vitamin,
    delete_vitamin,
)
from api.schemas.vitamin import Vitamin


@pytest.mark.asyncio
async def test_create_vitamin(
    mock_supabase_connection, example_vitamins_create, example_vitamins_response
):
    response = await create_vitamin(vitamin=example_vitamins_create[0])

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_update_vitamin(
    mock_supabase_connection,
    example_vitamins_injection,
    example_vitamins_update,
    example_vitamins_update_response,
):
    response = await update_vitamin(vitamin_id=1, vitamin=example_vitamins_update[0])

    assert response == example_vitamins_update_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_delete_vitamin(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await delete_vitamin(vitamin_id=1)

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)
