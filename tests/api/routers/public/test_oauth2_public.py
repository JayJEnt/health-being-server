import pytest

from api.authentication import email_authentication
from api.handlers.http_exceptions import UnknownProvider
from api.routers.public.oauth2_public import (
    login,
    auth_callback,
    login_with_form,
    register,
    send_email,
    verify_email,
)
from api.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_login_google(mock_redirect):
    await login("google")

    assert True


@pytest.mark.asyncio
async def test_login_unknown():
    with pytest.raises(UnknownProvider):
        await login("unknown")


@pytest.mark.asyncio
async def test_auth_callback(
    mock_async_client,
    mock_supabase_connection,
    mock_datetime_now,
    dummy_request,
    google_oauth2_expected_token,
):
    response = await auth_callback("google", dummy_request)

    assert response == google_oauth2_expected_token


@pytest.mark.asyncio
async def test_auth_callback_unknown(
    dummy_request,
):
    with pytest.raises(UnknownProvider):
        await auth_callback("unknown", dummy_request)


@pytest.mark.asyncio
async def test_login_with_form(
    mock_supabase_connection,
    mock_datetime_now,
    example_users_hashed_injection,
    example_form_data,
    expected_token_our_login,
):
    response = await login_with_form(example_form_data)

    assert response == expected_token_our_login


@pytest.mark.asyncio
async def test_our_register(
    mock_supabase_connection,
    mock_bcrypt,
    mock_datetime_now,
    mocked_email_postman,
    monkeypatch,
    example_users_register,
    example_users_hashed_response,
):
    monkeypatch.setattr(email_authentication, "email_postman", mocked_email_postman)
    requesting_user = UserCreate(**example_users_register[0])

    response = await register(requesting_user)

    assert response == example_users_hashed_response[0]


@pytest.mark.asyncio
async def test_send_email(
    mock_datetime_now,
    mocked_email_postman,
    monkeypatch,
):
    monkeypatch.setattr(email_authentication, "email_postman", mocked_email_postman)

    result = await send_email("test@example.com")

    assert result == {"message": "Verification email sent to test@example.com"}


@pytest.mark.asyncio
async def test_verify_email(
    mock_datetime_now_jwt,
    email_verification_token,
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    result = await verify_email(email_verification_token)

    assert result == example_users_response[0]
