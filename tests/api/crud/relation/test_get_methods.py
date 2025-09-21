import pytest

from api.crud.relation.get_methods import (
    get_relationship,
    get_relationships,
    get_relationships_and_related_tables,
    get_related_tables_items,
)
from api.handlers.http_exceptions import ResourceNotFound


@pytest.mark.asyncio
async def test_get_relationship(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_refrigerator_response,
):
    response = await get_relationship("user", 1, "refrigerator", 2)

    assert response == example_refrigerator_response[0]


@pytest.mark.asyncio
async def test_get_relationship_error(
    mock_supabase_connection, example_users_injection
):
    with pytest.raises(ResourceNotFound):
        await get_relationship("user", 1, "refrigerator", 1)


@pytest.mark.asyncio
async def test_get_relationships(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_refrigerator_response,
):
    response = await get_relationships("user", 1, "refrigerator")

    assert response == example_refrigerator_response


@pytest.mark.asyncio
async def test_get_relationships_error(
    mock_supabase_connection, example_users_injection
):
    with pytest.raises(ResourceNotFound):
        await get_relationships("user", 1, "refrigerator")


@pytest.mark.asyncio
async def test_get_relationships_and_related_tables_error(
    mock_supabase_connection, example_users_injection
):
    with pytest.raises(ResourceNotFound):
        await get_relationships_and_related_tables("user", 1, ["refrigerator"])


@pytest.mark.asyncio
async def test_get_related_tables_items(mock_supabase_connection):
    join_table_items = [
        {"user_id": 1, "ingredient_id": 1, "amount": 50},
    ]
    with pytest.raises(ResourceNotFound):
        await get_related_tables_items("user", "refrigerator", join_table_items)
