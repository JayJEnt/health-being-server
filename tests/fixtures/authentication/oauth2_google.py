from fastapi import Request

import pytest

from api.authentication import oauth2_google
from config import settings


@pytest.fixture
def mock_redirect(monkeypatch):
    class MockedRedirectResponse:
        def __init__(self, url: str, status_code: int = 302):
            self.url = url
            self.status_code = status_code

    monkeypatch.setattr(oauth2_google, "RedirectResponse", MockedRedirectResponse)


@pytest.fixture
def mock_google_secrets(monkeypatch):
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", "")
    monkeypatch.setattr(settings, "GOOGLE_REDIRECT_URI", "")


@pytest.fixture
def mock_async_client(monkeypatch):
    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

    class MockedAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, data=None):
            return MockResponse({"access_token": "token"})

        async def get(self, url, headers=None):
            return MockResponse(
                {
                    "name": "testuser",
                    "email": "test@example.com",
                    "access_token": "token",
                }
            )

    monkeypatch.setattr(
        oauth2_google, "httpx", type("httpx", (), {"AsyncClient": MockedAsyncClient})
    )


@pytest.fixture
def mock_async_client_no_token(monkeypatch):
    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

    class MockedAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, data=None):
            return MockResponse({})

        async def get(self, url, headers=None):
            return MockResponse({})

    monkeypatch.setattr(
        oauth2_google, "httpx", type("httpx", (), {"AsyncClient": MockedAsyncClient})
    )


@pytest.fixture
def dummy_request():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/auth/google/callback",
        "query_string": b"code=fake-code",
    }
    return Request(scope)


@pytest.fixture
def dummy_request_no_code():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/auth/google/callback",
        "query_string": "empty",
    }
    return Request(scope)


@pytest.fixture
def google_oauth2_expected_token():
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjksInVzZXJuYW1lIjoidGVzdHVzZXIiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJwcm92aWRlciI6Imdvb2dsZSIsImV4cCI6MTY3Mzc4NzAwMH0.BNMsAWQARk77M5yMGaz1tr0FHBqGGWqnv0EeMUr3o4s",
        "token_type": "bearer",
    }


@pytest.fixture
def google_oauth2_expected_token_exists():
    return {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0dXNlciIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsInByb3ZpZGVyIjoiZ29vZ2xlIiwiZXhwIjoxNjczNzg3MDAwfQ.cot6ZKL0aWmhKgwoj1H4xVeo_EPhhyLLBSmr6x6XPSg",
        "token_type": "bearer",
    }
