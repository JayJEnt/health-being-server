from sqlalchemy import create_engine

import pytest

from api.crud.single_entity import (
    delete_methods,
    get_methods,
    post_methods,
    put_methods,
    search_methods,
)
from api.crud.relation import (
    delete_methods as delete_relation, 
    get_methods as get_relation,
    post_methods as post_relation,
    put_methods as put_relation,
)
from api.crud.nested import (
    delete_methods as delete_nested,
    get_methods as get_nested,
    post_methods as post_nested,
    put_methods as put_nested,
)
from api.crud.many_entities import get_methods as get_all_methods
from database import supabase_connection
from database.supabase_connection import Base
from database import models
from config import settings


@pytest.fixture
def mocked_supabase_connection_init(monkeypatch):
    def mock_init(self):
        self.engine = create_engine(settings.TEST_DATABASE_URL)
        Base.metadata.create_all(self.engine)

    monkeypatch.setattr(supabase_connection.SupabaseConnection, "__init__", mock_init)

    test_supabase_connection = supabase_connection.SupabaseConnection()

    files_to_patch = [
        supabase_connection,

        post_methods,
        get_methods,
        delete_methods,
        put_methods,
        search_methods,

        post_relation,
        get_relation,
        delete_relation,
        put_relation,

        post_nested,
        get_nested,
        delete_nested,
        put_nested,

        get_all_methods,
    ]
    for file in files_to_patch:
        monkeypatch.setattr(file, "supabase_connection", test_supabase_connection)

    yield

    Base.metadata.drop_all(test_supabase_connection.engine)
    test_supabase_connection.engine.dispose()
