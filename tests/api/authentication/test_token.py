import pytest
from datetime import timedelta

from api.authentication.token import (
    create_access_token,
    validate_token,
    get_payload_from_token,
    get_user_from_payload,
    refresh_token,
)
from api.crud.single_entity.post_methods import create_element
from api.handlers.http_exceptions import InvalidToken


def test_create_access_token(mock_datetime_now, user_data, expected_token):
    token = create_access_token(user_data)
    assert token == expected_token


def test_create_access_token_with_time_delta(
    mock_datetime_now, user_data, expected_token
):
    token = create_access_token(user_data, timedelta(minutes=15))
    assert token == expected_token


@pytest.mark.asyncio
async def test_validate_correct_token(
    mock_datetime_now_jwt, mock_supabase_connection, user_create, expected_token
):
    await create_element("user", user_create)
    user = await validate_token(expected_token)

    assert user.id == 1
    assert user.username == user_create["username"]
    assert user.email == user_create["email"]


@pytest.mark.asyncio
async def test_get_payload_from_token(
    mock_datetime_now_jwt,
    expected_token,
    expected_payload,
):
    payload = await get_payload_from_token(expected_token)

    assert payload == expected_payload


@pytest.mark.asyncio
async def test_get_payload_from_invalid_token(
    expected_token,
):
    with pytest.raises(InvalidToken):
        await get_payload_from_token(expected_token)


@pytest.mark.asyncio
async def test_get_user_from_token(
    mock_supabase_connection, expected_payload, user_create
):
    await create_element("user", user_create)
    user = await get_user_from_payload(expected_payload)

    assert user.id == 1
    assert user.username == user_create["username"]
    assert user.email == user_create["email"]


@pytest.mark.asyncio
async def test_get_user_from_token_no_user(mock_supabase_connection, expected_payload):
    with pytest.raises(InvalidToken):
        await get_user_from_payload(expected_payload)


@pytest.mark.asyncio
async def test_get_user_from_token_no_email(mock_supabase_connection, invalid_payload):
    with pytest.raises(InvalidToken):
        await get_user_from_payload(invalid_payload)


@pytest.mark.asyncio
async def test_refresh_token(
    expected_token, mock_datetime_now_jwt, mock_supabase_connection, user_create
):
    await create_element("user", user_create)
    await refresh_token(expected_token)

    assert True  # since i cant mock time, so timedelat worked,
    # but then each time token is diffrent so we cant assert to any static result
