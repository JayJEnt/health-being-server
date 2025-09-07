from sqlalchemy import create_engine

import pytest

from api.handlers.exceptions import InternalServerError
from database.supabase_connection import SupabaseConnection, Base
from config import settings


@pytest.fixture()
def mocked_supabase_connection():
    class MockSupabaseConnection(SupabaseConnection):
        def __init__(self):
            self.engine = create_engine(settings.TEST_DATABASE_URL)
            Base.metadata.create_all(self.engine)

    conn = MockSupabaseConnection()
    yield conn
    conn.engine.dispose()


@pytest.fixture()
def mocked_supabase_connection_error():
    class MockSupabaseConnection(SupabaseConnection):
        def __init__(self):
            self.engine = create_engine(settings.TEST_DATABASE_URL)
            Base.metadata.create_all(self.engine)

        def execute_query(self, query):
            raise InternalServerError

    conn = MockSupabaseConnection()
    yield conn
    conn.engine.dispose()
