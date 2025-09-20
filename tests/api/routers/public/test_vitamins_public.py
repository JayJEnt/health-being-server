import pytest

from api.routers.public.vitamins_public import get_vitamins
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
async def test_get_vitamin_by_name(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await get_vitamins(vitamin_name="C")

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)


@pytest.mark.asyncio
async def test_get_vitamin(
    mock_supabase_connection, example_vitamins_injection, example_vitamins_response
):
    response = await get_vitamins(vitamin_id=1)

    assert response == example_vitamins_response[0]

    parsed = Vitamin(**response)

    assert isinstance(parsed, Vitamin)
