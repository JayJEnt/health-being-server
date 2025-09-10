import pytest

from api.authentication.hash_methods import bcrypt


@pytest.fixture
def password():
    return "Password"


@pytest.fixture
def wrong_password():
    return "FakePassword"


@pytest.fixture
def hashed_password():
    return "$2b$12$9VpQw6INCOS9B98cgHSVse8bqF7zx5x2z1BvOUVoRckisrVV7nFUu"


@pytest.fixture
def mock_bcrypt(monkeypatch):
    def mock_gensalt():
        return b"$2b$12$9VpQw6INCOS9B98cgHSVse"

    monkeypatch.setattr(bcrypt, "gensalt", mock_gensalt)
