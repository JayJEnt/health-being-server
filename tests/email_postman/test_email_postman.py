import pytest

from api.handlers.http_exceptions import InternalServerError


def test_email_postman_init_success(mocked_email_postman):
    assert isinstance(mocked_email_postman._server, object)


def test_email_postman_login_failure(mocked_email_postman_login_failure):
    with pytest.raises(ConnectionRefusedError):
        mocked_email_postman_login_failure()


def test_create_message_content(mocked_email_postman):
    msg = mocked_email_postman.create_message(
        email="test@example.com", subject="Test", body="<p>Test!</p>"
    )

    assert msg["Subject"] == "Test"
    assert msg["To"] == "test@example.com"
    assert msg.get_content_type() == "multipart/alternative"


def test_send_message_success(mocked_email_postman, mock_test_email_message):
    mocked_email_postman.send_message(mock_test_email_message)

    assert True


def test_send_message_failure(
    mocked_email_postman_send_failure, mock_test_email_message
):
    with pytest.raises(InternalServerError):
        mocked_email_postman_send_failure.send_message(mock_test_email_message)
