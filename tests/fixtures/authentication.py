import pytest
from datetime import datetime
from unittest.mock import MagicMock

# HASH METHODS
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
    from api.authentication.hash_methods import bcrypt
    def mock_gensalt():
        return b'$2b$12$9VpQw6INCOS9B98cgHSVse'
    
    monkeypatch.setattr(bcrypt, 'gensalt', mock_gensalt)


# TOKEN
@pytest.fixture
def mock_datetime_utcnow(monkeypatch):
    from api.authentication import token

    fixed_time = datetime(2023, 1, 15, 12, 0, 0)
    mock_dt = MagicMock()
    mock_dt.utcnow.return_value = fixed_time
    monkeypatch.setattr(token, 'datetime', mock_dt)
    
    return fixed_time


@pytest.fixture
def user_data():
    return {
        "id": 420,
        "username": "test_user",
        "sub": "test.user@example.com",
        "provider": "health-being-server"
    }


@pytest.fixture
def expected_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDIwLCJ1c2VybmFtZSI6InRlc3RfdXNlciIsInN1YiI6InRlc3QudXNlckBleGFtcGxlLmNvbSIsInByb3ZpZGVyIjoiaGVhbHRoLWJlaW5nLXNlcnZlciIsImV4cCI6MTY3Mzc4NDkwMH0.1-RirvhltrGMvB_YApDS9bd9T4YFs4DbnczHH4PRfjk"


# @pytest.fixture
# def mock_supabase(monkeypatch, user_data):
#     from api.authentication import token

#     monkeypatch.setattr(token, 'get_element_by_name', user_data)