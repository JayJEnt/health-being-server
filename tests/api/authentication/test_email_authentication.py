import pytest

from api.authentication import email_authentication


@pytest.mark.asyncio
async def test_create_email_verification_token(
    mock_datetime_now, fake_email_verification_token
):
    token = await email_authentication.create_email_verification_token(
        "test@example.com", 15
    )

    assert token == fake_email_verification_token


@pytest.mark.asyncio
async def test_send_verification_email(
    mock_datetime_now, mocked_email_postman, monkeypatch
):
    monkeypatch.setattr(email_authentication, "email_postman", mocked_email_postman)
    result = await email_authentication.send_verification_email("test@example.com")

    assert result == {"message": "Verification email sent to test@example.com"}
