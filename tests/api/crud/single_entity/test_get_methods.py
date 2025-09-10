import pytest

from api.crud.single_entity.get_methods import (
    get_elements,
    get_element_by_name,
    get_element_by_id,
)


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
    with pytest.raises(Exception) as excinfo:
        await get_element_by_name("user", "New User")

    assert str(excinfo.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_get_element_by_name_error_2(
    mock_supabase_connection, example_users_injection
):
    with pytest.raises(Exception) as excinfo:
        await get_element_by_name("user", "New")

    assert str(excinfo.value) == "404: Requested resource not found"


@pytest.mark.asyncio
async def test_get_element_by_id(
    mock_supabase_connection, example_users_injection, example_users_response
):
    response = await get_element_by_id("user", 1)

    assert response == example_users_response[0]


@pytest.mark.asyncio
async def test_get_element_by_id_error(mock_supabase_connection):
    with pytest.raises(Exception) as excinfo:
        await get_element_by_id("user", 999)

    assert str(excinfo.value) == "404: Requested resource not found"
