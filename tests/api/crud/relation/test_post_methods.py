import pytest

from api.crud.relation.post_methods import create_relationship, create_relationships
from api.handlers.http_exceptions import (
    ResourceNotFound,
    ReferencesToItself,
    ResourceAlreadyTaken,
)


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
    with pytest.raises(ResourceNotFound):
        await create_relationship(
            "user", 1, "refrigerator", example_refrigerator_create[0]
        )


@pytest.mark.asyncio
async def test_create_relationship_error_reference_to_itself(
    mock_supabase_connection, example_users_injection, example_users_create
):
    with pytest.raises(ReferencesToItself):
        await create_relationship("user", 1, "user", example_users_create[0])


@pytest.mark.asyncio
async def test_create_relationship_error_rescource_already_taken(
    mock_supabase_connection,
    example_ingredients_injection,
    example_refrigerator_create,
    example_refrigerator_create_response,
):
    await create_relationship("user", 1, "refrigerator", example_refrigerator_create[0])
    with pytest.raises(ResourceAlreadyTaken):
        await create_relationship(
            "user", 1, "refrigerator", example_refrigerator_create[0]
        )


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
