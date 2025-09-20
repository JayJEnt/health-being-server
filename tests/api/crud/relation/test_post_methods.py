import pytest

from api.crud.relation.post_methods import create_relationship, create_relationships


@pytest.mark.asyncio
async def test_create_relationship(
    mock_supabase_connection,
    example_ingredients_injection,
    example_refrigerator_create,
    example_refrigerator_create_response,
):
    response = await create_relationship(
        "user", 1, "refrigerator", example_refrigerator_create[0]
    )

    assert response == example_refrigerator_create_response[0]


@pytest.mark.asyncio
async def test_create_relationship_error_not_found(
    mock_supabase_connection, example_refrigerator_create
):
    with pytest.raises(Exception) as e_info:
        await create_relationship(
            "user", 1, "refrigerator", example_refrigerator_create[0]
        )

    assert str(e_info.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_create_relationship_error_reference_to_itself(
    mock_supabase_connection, example_users_injection, example_users_create
):
    with pytest.raises(Exception) as e_info:
        await create_relationship("user", 1, "user", example_users_create[0])

    assert str(e_info.value) == "405: Referencing to itself is not allowed"


@pytest.mark.asyncio
async def test_create_relationships(
    mock_supabase_connection,
    example_ingredients_injection,
    example_refrigerator_create,
    example_refrigerator_create_response,
):
    response = await create_relationships(
        "user", 1, [{"refrigerator": example_refrigerator_create}]
    )

    assert response == [{"refrigerator": example_refrigerator_create_response}]
