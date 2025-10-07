import pytest

from api.crud.many_entities.post_methods import create_all
from api.handlers.http_exceptions import ResourceNotFound


@pytest.mark.asyncio
async def test_post_all_elements(
    mock_supabase_connection,
    example_diet_types_injection,
    example_ingredients_injection,
    example_recipes_create_all,
    example_recipes_response_all,
):
    response = await create_all(
        "recipes",
        example_recipes_create_all[0],
        related_attributes=["ingredients", "diet_type"],
    )

    assert response == example_recipes_response_all


@pytest.mark.asyncio
async def test_post_all_elements_error_resource_not_found(
    mock_supabase_connection, example_recipes_create_all
):
    with pytest.raises(ResourceNotFound):
        await create_all(
            "recipes",
            example_recipes_create_all[0],
            related_attributes=["ingredients", "diet_type"],
        )
