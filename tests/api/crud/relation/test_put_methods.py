import pytest

from api.crud.relation.put_methods import update_relationships


@pytest.mark.asyncio
async def test_update_relationships(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_refrigerator_update,
    example_refrigerator_update_response,
):
    response = await update_relationships(
        "user", 1, [{"refrigerator": example_refrigerator_update}]
    )

    assert response == [{"refrigerator": example_refrigerator_update_response}]


@pytest.mark.asyncio
async def test_update_relationships_error(
    mock_supabase_connection, example_refrigerator_update
):
    response = await update_relationships(
        "user", 999, [{"refrigerator": example_refrigerator_update}]
    )

    assert response == [{"refrigerator": [None, None]}]
