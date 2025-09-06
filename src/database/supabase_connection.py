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

from api.handlers.exceptions import ResourceNotFound, InternalServerError
from config import settings
from logger import logger


Base = declarative_base()


class SupabaseConnection:
    def __init__(self):
        self.engine = create_engine(
            settings.SUPABASE_URL, pool_size=1, max_overflow=0, future=True
        )

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


supabase_connection = SupabaseConnection()
