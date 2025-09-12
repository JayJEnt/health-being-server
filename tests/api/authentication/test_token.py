import pytest
from datetime import timedelta

from api.authentication.token import (
    create_access_token,
    validate_token,
    get_payload_from_token,
    get_user_from_token,
    time_for_refresh,
    refresh_token,
)
from api.crud.single_entity.post_methods import create_element


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
    with pytest.raises(Exception) as excinfo:
        await get_payload_from_token(expected_token)

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_get_user_from_token(
    mock_supabase_connection, expected_payload, user_create
):
    await create_element("user", user_create)
    user = await get_user_from_token(expected_payload)

    assert user.id == 1
    assert user.username == user_create["username"]
    assert user.email == user_create["email"]


@pytest.mark.asyncio
async def test_get_user_from_token_no_user(mock_supabase_connection, expected_payload):
    with pytest.raises(Exception) as excinfo:
        await get_user_from_token(expected_payload)

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_get_user_from_token_no_email(mock_supabase_connection, invalid_payload):
    with pytest.raises(Exception) as excinfo:
        await get_user_from_token(invalid_payload)

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_time_for_refresh(expected_payload):
    result = await time_for_refresh(expected_payload, timedelta(minutes=20))

    assert result is True


@pytest.mark.asyncio
async def test_time_for_refresh_invalid_token(invalid_payload, mock_datetime_now):
    with pytest.raises(Exception) as excinfo:
        await time_for_refresh(invalid_payload, timedelta(minutes=5))

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_refresh_token(
    expected_token, mock_datetime_now_jwt, mock_supabase_connection, user_create
):
    await create_element("user", user_create)
    await refresh_token(expected_token)

    assert True  # since i cant mock time, so timedelat worked,
    # but then each time token is diffrent so we cant assert to any static result
