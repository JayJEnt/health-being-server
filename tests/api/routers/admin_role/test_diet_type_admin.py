import pytest

from api.routers.admin_role.diet_types_admin import (
    create_diet_type,
    update_diet_type,
    delete_diet_type,
)
from api.schemas.diet_type import DietType


@pytest.mark.asyncio
async def test_create_diet_type(
    mock_supabase_connection, example_diet_types_create, example_diet_types_response
):
    response = await create_diet_type(example_diet_types_create[0])

    assert response == example_diet_types_response[0]

    parsed = DietType(**response)

    assert isinstance(parsed, DietType)


@pytest.mark.asyncio
async def test_update_diet_type(
    mock_supabase_connection,
    example_diet_types_injection,
    example_diet_types_update,
    example_diet_types_update_response,
):
    response = await update_diet_type(
        diet_type=example_diet_types_update[0], diet_type_id=1
    )

    assert response == example_diet_types_update_response[0]

    parsed = DietType(**response)

    assert isinstance(parsed, DietType)


@pytest.mark.asyncio
async def test_delete_diet_type(
    mock_supabase_connection, example_diet_types_injection, example_diet_types_response
):
    response = await delete_diet_type(diet_type_id=1)

    assert response == example_diet_types_response[0]

    parsed = DietType(**response)

    assert isinstance(parsed, DietType)
