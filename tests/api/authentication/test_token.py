import pytest
from datetime import timedelta

from api.authentication.token import create_access_token, validate_token
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
    mock_datetime_utcnow, mocked_supabase_connection, user_create, expected_token
):
    await create_element("user", user_create)
    user = await validate_token(expected_token)

    assert user.id == 1
    assert user.username == user_create["username"]
    assert user.email == user_create["email"]


@pytest.mark.asyncio
async def test_validate_correct_token_no_email(expected_token):
    with pytest.raises(Exception) as excinfo:
        await validate_token(expected_token)

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_validate_correct_token_invalid_token(
    mock_datetime_utcnow, invalid_token
):
    with pytest.raises(Exception) as excinfo:
        await validate_token(invalid_token)

    assert str(excinfo.value) == "401: Could not validate credentials"


@pytest.mark.asyncio
async def test_validate_correct_token_no_user(
    mock_datetime_utcnow, mocked_supabase_connection, expected_token
):
    with pytest.raises(Exception) as excinfo:
        await validate_token(expected_token)

    assert str(excinfo.value) == "401: Could not validate credentials"
