import pytest

from api.authentication.oauth2_google import google_login, google_auth_callback


@pytest.mark.asyncio
async def test_google_login(mock_redirect):
    await google_login()

    assert True


@pytest.mark.asyncio
async def test_google_login_no_google_secrets(mock_google_secrets):
    with pytest.raises(Exception) as exc_info:
        await google_login()

    assert str(exc_info.value) == "Missing required Google OAuth environment variables"


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
    with pytest.raises(Exception) as exc_info:
        await google_auth_callback(dummy_request_no_code)

    assert str(exc_info.value) == "404: Authorization code not found"


@pytest.mark.asyncio
async def test_google_auth_callback_no_token(
    mock_async_client_no_token,
    mock_datetime_now,
    dummy_request,
    google_oauth2_expected_token,
):
    with pytest.raises(Exception) as exc_info:
        await google_auth_callback(dummy_request)

    assert str(exc_info.value) == "400: Failed to retrieve access token"


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
