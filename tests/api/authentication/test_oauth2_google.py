import pytest

from api.authentication.oauth2_google import google_login, google_auth_callback
from api.handlers.http_exceptions import AuthorizationCodeNotFound, TokenNotRecived
from api.handlers.custom_exceptions import MissingVariables


@pytest.mark.asyncio
async def test_google_login(mock_redirect):
    await google_login()

    assert True


@pytest.mark.asyncio
async def test_google_login_no_google_secrets(mock_google_secrets):
    with pytest.raises(MissingVariables):
        await google_login()


@pytest.mark.asyncio
async def test_google_auth_callback(
    mock_async_client,
    mock_supabase_connection,
    mock_datetime_now,
    dummy_request,
    google_oauth2_expected_token,
):
    response = await google_auth_callback(dummy_request)

    assert response == google_oauth2_expected_token


@pytest.mark.asyncio
async def test_google_auth_callback_bad_request(dummy_request_no_code):
    with pytest.raises(AuthorizationCodeNotFound):
        await google_auth_callback(dummy_request_no_code)


@pytest.mark.asyncio
async def test_google_auth_callback_no_token(
    mock_async_client_no_token,
    mock_datetime_now,
    dummy_request,
    google_oauth2_expected_token,
):
    with pytest.raises(TokenNotRecived):
        await google_auth_callback(dummy_request)


@pytest.mark.asyncio
async def test_google_auth_callback_user_exists(
    mock_async_client,
    mock_datetime_now,
    mock_supabase_connection,
    example_users_injection,
    dummy_request,
    google_oauth2_expected_token_exists,
):
    response = await google_auth_callback(dummy_request)

    assert response == google_oauth2_expected_token_exists
