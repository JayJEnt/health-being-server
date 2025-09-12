import pytest
from datetime import datetime, timezone

from api.authentication import token
from jose import jwt


@pytest.fixture
def mock_datetime_now(monkeypatch):
    fixed_time = datetime(2023, 1, 15, 12, 20, 0, tzinfo=timezone.utc)

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            if tz:
                return fixed_time.astimezone(tz)
            return fixed_time

    monkeypatch.setattr(token, "datetime", FixedDatetime)


@pytest.fixture
def mock_datetime_now_jwt(monkeypatch):
    fixed_time = datetime(2023, 1, 15, 12, 20, 0, tzinfo=timezone.utc)

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            if tz:
                return fixed_time.astimezone(tz)
            return fixed_time

    monkeypatch.setattr(jwt, "datetime", FixedDatetime)


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "username": "test_user",
        "sub": "test.user@example.com",
        "provider": "health-being-server",
    }


@pytest.fixture
def user_create():
    return {
        "username": "test_user",
        "email": "test.user@example.com",
        "hashed_password": "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu",
        "role": "admin",
    }


@pytest.fixture
def expected_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJzdWIiOiJ0ZXN0LnVzZXJAZXhhbXBsZS5jb20iLCJwcm92aWRlciI6ImhlYWx0aC1iZWluZy1zZXJ2ZXIiLCJleHAiOjE2NzM3ODYxMDB9.OHo3h13hgBzPMU3cWIiqCO-pg-8eNcl93oKbfswtqik"


@pytest.fixture
def invalid_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJwcm92aWRlciI6ImhlYWx0aC1iZWluZy1zZXJ2ZXIiLCJleHAiOjE2NzM3ODQ5MDB9.ilyfBuDrBoZbBSUYPCMItsy8tHTqJVywxiA1bK3dvCk"


@pytest.fixture
def expected_payload():
    return {
        "exp": 1673786100,
        "id": 1,
        "provider": "health-being-server",
        "sub": "test.user@example.com",
        "username": "test_user",
    }


@pytest.fixture
def invalid_payload():
    return {
        "id": 1,
        "provider": "health-being-server",
        "username": "test_user",
    }
