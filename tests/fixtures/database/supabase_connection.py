from sqlalchemy import (
    Table,
    MetaData,
    select,
    insert,
    update,
    delete,
    and_,
    create_engine,
)
from sqlalchemy.orm import declarative_base

from typing import Any, Dict, Optional, List
from functools import wraps
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
from api.handlers.http_exceptions import InternalServerError
from api.handlers.http_exceptions import ResourceNotFound
from database import supabase_connection
from config import settings
from logger import logger


Base = declarative_base()


class MockSupabaseConnection:
    def __init__(self):
        self.engine = create_engine(settings.TEST_DATABASE_URL)

    @staticmethod
    def error_handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Processing request: {func.__name__}")
                result = func(*args, **kwargs)
                if result is None:
                    func_args = (
                        args[1:]
                        if args and args[0].__class__.__name__ == "SupabaseConnection"
                        else args
                    )
                    logger.info(
                        f"Resource not found - Operation: {func.__name__}, "
                        f"Args: {func_args}"
                    )
                    raise ResourceNotFound
                logger.info("Successfully processed.")
                return result
            except ResourceNotFound:
                raise ResourceNotFound
            except Exception as ex:
                logger.error(f"Supabase error: {ex}")
                raise InternalServerError

        return wrapper

    def execute_query(self, query: Any) -> Optional[List[Dict[str, Any]]]:
        with self.engine.begin() as conn:
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]
        return rows or None

    """CRUD"""

    @error_handler
    def fetch_all(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = select(table)

        return self.execute_query(query)

    @error_handler
    def insert(self, table_name: str, data: dict) -> Optional[Dict[str, Any]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = insert(table).values(data).returning(table)

        rows = self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    def find_by(
        self, table_name: str, column: str, value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = select(table).where(table.c[column] == value)

        return self.execute_query(query)

    @error_handler
    def find_join_record(
        self,
        table_name: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = select(table).where(
            and_(
                table.c[first_column] == first_value,
                table.c[second_column] == second_value,
            )
        )

        rows = self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    def find_ilike(
        self, table_name: str, column: str, value: str
    ) -> Optional[List[Dict[str, Any]]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = select(table).where(table.c[column].ilike(f"%{value}%"))

        return self.execute_query(query)

    @error_handler
    def delete_by(
        self, table_name: str, column: str, value: Any
    ) -> Optional[Dict[str, Any]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = delete(table).where(table.c[column] == value).returning(table)

        rows = self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    def delete_join_record(
        self,
        table_name: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = (
            delete(table)
            .where(
                and_(
                    table.c[first_column] == first_value,
                    table.c[second_column] == second_value,
                )
            )
            .returning(table)
        )

        rows = self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    def update_by(
        self, table_name: str, column: str, value: Any, updates: dict
    ) -> Optional[Dict[str, Any]]:
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        query = (
            update(table)
            .where(table.c[column] == value)
            .values(updates)
            .returning(table)
        )

        rows = self.execute_query(query)
        return rows[0] if rows else None


@pytest.fixture
def mock_supabase_connection(monkeypatch):
    test_supabase_connection = MockSupabaseConnection()
    Base.metadata.create_all(test_supabase_connection.engine)

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


@pytest.fixture
def mocked_supabase_connection(input_data):
    class FakeSupabaseClient:
        def table(self, *args, **kwargs):
            return self

        def select(self, *args, **kwargs):
            return self

        def insert(self, *args, **kwargs):
            return self

        def update(self, *args, **kwargs):
            return self

        def delete(self, *args, **kwargs):
            return self

        def eq(self, *args, **kwargs):
            return self

        def ilike(self, *args, **kwargs):
            return self

        def execute(self, *args, **kwargs):
            return type("Response", (), {"data": input_data})()

    conn = supabase_connection.SupabaseConnection()
    conn._client = FakeSupabaseClient()

    return conn


@pytest.fixture
def mocked_supabase_connection_wrong_credentials(monkeypatch):
    def mocked_create_client(*args, **kwargs):
        raise ConnectionRefusedError

    monkeypatch.setattr(supabase_connection, "create_client", mocked_create_client)

    return supabase_connection.SupabaseConnection


@pytest.fixture
def broken_supabase_connection():
    class BrokenSupabaseClient:
        def table(self, *args, **kwargs):
            return self

        def select(self, *args, **kwargs):
            return self

        def execute(self, *args, **kwargs):
            raise RuntimeError()

    conn = supabase_connection.SupabaseConnection()
    conn._client = BrokenSupabaseClient()

    return conn
