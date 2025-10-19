import pytest

from api.authentication import email_authentication
from api.handlers.http_exceptions import InvalidToken


@pytest.mark.asyncio
async def test_create_email_verification_token(
    mock_datetime_now, email_verification_token
):
    token = await email_authentication.create_email_verification_token(
        "test@example.com", 15
    )

    assert token == email_verification_token


@pytest.mark.asyncio
async def test_send_verification_email(
    mock_datetime_now, mocked_email_postman, monkeypatch
):
    monkeypatch.setattr(email_authentication, "email_postman", mocked_email_postman)
    result = await email_authentication.send_verification_email("test@example.com")

    assert result == {"message": "Verification email sent to test@example.com"}


@pytest.mark.asyncio
async def test_verify_email_token(
    mock_datetime_now_jwt,
    email_verification_token,
    mock_supabase_connection,
    example_users_injection,
    example_users_response,
):
    result = await email_authentication.verify_email_token(email_verification_token)
    assert result == example_users_response[0]


@pytest.mark.asyncio
async def test_verify_email_token_invalid_type(
    mock_datetime_now_jwt, invalid_email_verification_token
):
    with pytest.raises(InvalidToken):
        await email_authentication.verify_email_token(invalid_email_verification_token)


@pytest.mark.asyncio
async def test_verify_email_token_resource_not_found(
    mock_datetime_now_jwt, email_verification_token, mock_supabase_connection
):
    with pytest.raises(InvalidToken):
        await email_authentication.verify_email_token(email_verification_token)
