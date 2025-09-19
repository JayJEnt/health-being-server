import pytest

from api.routers.public.oauth2_public import (
    login,
    auth_callback,
    login_with_form,
    our_register,
)
from api.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_login_google(mock_redirect):
    await login("google")

    assert True


@pytest.mark.asyncio
async def test_login_unknown():
    with pytest.raises(Exception) as exc_info:
        await login("unknown")

    assert str(exc_info.value) == "404: Unknown provider"


@pytest.mark.asyncio
async def test_auth_callback(
    mock_async_client,
    mock_supabase_connection,
    mock_datetime_now,
    dummy_request,
    google_oauth2_expected_token,
):
    response = await auth_callback(dummy_request)

    assert response == google_oauth2_expected_token


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
    example_users_register,
    example_users_hashed_response,
):
    requesting_user = UserCreate(**example_users_register[0])

    response = await our_register(requesting_user)

    assert response == example_users_hashed_response[0]
