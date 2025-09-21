import pytest

from api.authentication.oauth2_our import authenticate_user, our_login, register
from api.handlers.http_exceptions import InvalidCredentials
from api.schemas.user import UserOurAuth, UserCreate


@pytest.mark.asyncio
async def test_authenticate_user(
    mock_supabase_connection,
    example_users_hashed_injection,
    example_users_create,
    example_users_hashed_response,
):
    response = await authenticate_user(
        example_users_create[0]["email"], example_users_create[0]["hashed_password"]
    )

    assert response == UserOurAuth(**example_users_hashed_response[0])

    assert isinstance(response, UserOurAuth)


@pytest.mark.asyncio
async def test_authenticate_user_no_user(
    mock_supabase_connection, example_users_create
):
    response = await authenticate_user(
        example_users_create[0]["email"], example_users_create[0]["hashed_password"]
    )

    assert response is False


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(
    mock_supabase_connection, example_users_hashed_injection, example_users_create
):
    response = await authenticate_user(
        example_users_create[0]["email"], "fake_password"
    )

    assert response is False


@pytest.mark.asyncio
async def test_our_login(
    mock_supabase_connection,
    mock_datetime_now,
    example_users_hashed_injection,
    example_form_data,
    expected_token_our_login,
):

    response = await our_login(example_form_data)

    assert response == expected_token_our_login


@pytest.mark.asyncio
async def test_our_login_error(
    mock_supabase_connection,
    mock_datetime_now,
    example_users_hashed_injection,
    example_form_data_error,
    expected_token_our_login,
):
    with pytest.raises(InvalidCredentials):
        await our_login(example_form_data_error)


@pytest.mark.asyncio
async def test_register(
    mock_supabase_connection,
    mock_bcrypt,
    example_users_register,
    example_users_hashed_response,
):
    requesting_user = UserCreate(**example_users_register[0])

    response = await register(requesting_user)

    assert response == example_users_hashed_response[0]


@pytest.mark.asyncio
async def test_register_already_exists(
    mock_supabase_connection,
    example_users_hashed_injection,
    example_users_register,
    example_users_hashed_response,
):
    requesting_user = UserCreate(**example_users_register[0])

    response = await register(requesting_user)

    assert response == example_users_hashed_response[0]
