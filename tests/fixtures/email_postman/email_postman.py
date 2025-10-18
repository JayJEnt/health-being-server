import pytest
from email_postman import email_postman


@pytest.fixture
def mocked_email_postman(monkeypatch):
    class FakeSMTP:
        def starttls(self, *args, **kwargs):
            return self

        def login(self, *args, **kwargs):
            return self

        def send_message(self, *args, **kwargs):
            self.sent = True
            return {"status": "ok"}

    monkeypatch.setattr(email_postman, "SMTP", lambda *a, **k: FakeSMTP())
    return email_postman.EmailPostman()


@pytest.fixture
def mocked_email_postman_login_failure(monkeypatch):
    class FakeSMTP:
        def starttls(self, *args, **kwargs):
            return self

        def login(self, *args, **kwargs):
            raise Exception("Login failed")

    monkeypatch.setattr(email_postman, "SMTP", lambda *a, **k: FakeSMTP())
    return email_postman.EmailPostman


@pytest.fixture
def mocked_email_postman_send_failure(monkeypatch):
    class FakeSMTP:
        def starttls(self, *args, **kwargs):
            return self

        def login(self, *args, **kwargs):
            return self

        def send_message(self, *args, **kwargs):
            raise RuntimeError("Send failed")

    monkeypatch.setattr(email_postman, "SMTP", lambda *a, **k: FakeSMTP())
    return email_postman.EmailPostman()


@pytest.fixture
def mock_test_email_message(mocked_email_postman):
    msg = mocked_email_postman.create_message("test@example.com", "test", "body")
    return msg
