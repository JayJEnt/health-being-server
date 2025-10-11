import pytest

from api.routers.public.diet_types_public import get_diet_types
from api.schemas.diet_type import DietTypeResponse


@pytest.mark.asyncio
async def test_get_diet_types(
    mock_supabase_connection, example_diet_types_injection, example_diet_types_response
):
    response = await get_diet_types()

    assert response == example_diet_types_response
    assert isinstance(response, list)

    for item in response:
        parsed = DietTypeResponse(**item)

        assert isinstance(parsed, DietTypeResponse)


@pytest.mark.asyncio
async def test_get_diet_type(
    mock_supabase_connection, example_diet_types_injection, example_diet_types_response
):
    response = await get_diet_types(diet_type_id=1)

    assert response == example_diet_types_response[0]

    parsed = DietTypeResponse(**response)

    assert isinstance(parsed, DietTypeResponse)


@pytest.mark.asyncio
async def test_get_diet_by_name(
    mock_supabase_connection, example_diet_types_injection, example_diet_types_response
):
    response = await get_diet_types(diet_name="VeGan")

    assert response == example_diet_types_response[1]

    parsed = DietTypeResponse(**response)

    assert isinstance(parsed, DietTypeResponse)


@pytest.mark.asyncio
async def test_search_diet_types_by_phrase(
    mock_supabase_connection, example_diet_types_injection, example_diet_types_response
):

    response = await get_diet_types(search_phrase="vega")

    assert response == [example_diet_types_response[1]]

    parsed = DietTypeResponse(**response[0])

    assert isinstance(parsed, DietTypeResponse)
