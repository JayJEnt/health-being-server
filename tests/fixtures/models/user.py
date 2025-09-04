import pytest

from database.models.user import User


@pytest.fixture()
def example_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="password",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user