import pytest

from api.routers.vitamins import (
    get_vitamins,
    get_vitamin,
    get_vitamin_by_name,
    create_vitamin,
    update_vitamin,
    delete_vitamin,
)
from api.schemas.vitamin import Vitamin


@pytest.mark.asyncio
async def test_get_vitamins(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await get_vitamins()

    assert response == example_vitamins_response
    assert isinstance(response, list)

    for item in response:
        parsed = Vitamin(**item)

        assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_get_vitamin(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await get_vitamin(1)

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_get_vitamin_by_name(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await get_vitamin_by_name("C")

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_create_vitamin(
    mock_supabase_connection, example_vitamins_create, example_vitamins_response
):
    response = await create_vitamin(example_vitamins_create[0])

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
    response = await update_vitamin(1, example_vitamins_update[0])

    assert response == example_vitamins_update_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_delete_vitamin(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await delete_vitamin(1)

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)
