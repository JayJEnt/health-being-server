from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from database.models.user import User
from database.supabase_connection import Base
from config import settings


@pytest.fixture()
def db_engine():
    engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()
