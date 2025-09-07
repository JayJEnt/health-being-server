import pytest

from api.crud.relation.delete_methods import delete_relationship, delete_relationships


@pytest.mark.asyncio
async def test_delete_relationship(
    mock_supabase_connection,
    example_refrigerator_injection,
    example_refrigerator_response,
):
    response = await delete_relationship("user", 1, "refrigerator", 2)

    assert response == example_refrigerator_response[0]


@pytest.mark.asyncio
async def test_delete_relationship_error_not_found(mock_supabase_connection):
    with pytest.raises(Exception) as e_info:
        await delete_relationship("user", 1, "refrigerator", 1)

    assert str(e_info.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_create_relationships(
    mock_supabase_connection, example_refrigerator_injection
):
    await delete_relationships("user", 1, ["refrigerator"])

    assert True  # delete_relationships does not return anything


@pytest.mark.asyncio
async def test_delete_relationships_error_not_found(mock_supabase_connection):
    await delete_relationships("user", 1, ["refrigerator"])

    assert True  # delete_relationships does not return anything and does not raise an error
