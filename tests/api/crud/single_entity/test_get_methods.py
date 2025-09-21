import pytest

from api.crud.single_entity.get_methods import (
    get_elements,
    get_element_by_name,
    get_element_by_id,
    is_duplicated,
)
from api.handlers.http_exceptions import ResourceNotFound, ResourceAlreadyTaken


@pytest.mark.asyncio
async def test_get_elements(
    mock_supabase_connection, example_users_injection, example_users_response
):
    response = await get_elements("user")

    assert response == example_users_response


@pytest.mark.asyncio
async def test_get_elements_restricted(
    mock_supabase_connection,
    example_recipes_injection,
    example_recipes_overview_response,
):
    response = await get_elements("recipes", restrict=True)

    assert response == example_recipes_overview_response


@pytest.mark.asyncio
async def test_get_element_by_name(
    mock_supabase_connection, example_users_injection, example_users_response
):
    response = await get_element_by_name("user", "New User")

    assert response == example_users_response[1]


@pytest.mark.asyncio
async def test_get_element_by_alternative_name(
    mock_supabase_connection, example_users_injection, example_users_response
):
    response = await get_element_by_name(
        "user", "newuser@example.com", alternative_name=True
    )

    assert response == example_users_response[1]


@pytest.mark.asyncio
async def test_get_element_by_name_error(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await get_element_by_name("user", "New User")


@pytest.mark.asyncio
async def test_get_element_by_name_error_2(
    mock_supabase_connection, example_users_injection
):
    with pytest.raises(ResourceNotFound):
        await get_element_by_name("user", "New")


@pytest.mark.asyncio
async def test_get_element_by_id(
    mock_supabase_connection, example_users_injection, example_users_response
):
    response = await get_element_by_id("user", 1)

    assert response == example_users_response[0]


@pytest.mark.asyncio
async def test_get_element_by_id_error(mock_supabase_connection):
    with pytest.raises(ResourceNotFound):
        await get_element_by_id("user", 999)


@pytest.mark.asyncio
async def test_is_duplicated_by_id(mock_supabase_connection, example_users_injection):
    with pytest.raises(ResourceAlreadyTaken):
        await is_duplicated("user", 1)


@pytest.mark.asyncio
async def test_is_duplicated_by_name(mock_supabase_connection, example_users_injection):
    with pytest.raises(ResourceAlreadyTaken):
        await is_duplicated("user", "New User")


@pytest.mark.asyncio
async def test_is_not_duplicated(mock_supabase_connection):
    await is_duplicated("user", "New User")

    assert True  # Hasn't triggered any exceptions
