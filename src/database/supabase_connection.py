from sqlalchemy import (
    Table,
    MetaData,
    select,
    insert,
    update,
    delete,
    and_,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from typing import Any, Dict, Optional, List
from functools import wraps

from api.handlers.exceptions import ResourceNotFound, InternalServerError
from config import settings
from logger import logger


Base = declarative_base()


class SupabaseConnection:
    def __init__(self):
        self.engine = create_async_engine(
            settings.SUPABASE_URL,
            pool_size=10,
            max_overflow=5,
            future=True,
            connect_args={"statement_cache_size": 0},
        )
        self._tables = {}

    @staticmethod
    def error_handler(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"Processing request: {func.__name__}")
                result = await func(*args, **kwargs)
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
        
    async def get_table(self, table_name: str) -> Table:
        if table_name in self._tables:
            return self._tables[table_name]

        async with self.engine.connect() as conn:
            def load_table(sync_conn):
                return Table(table_name, MetaData(), autoload_with=sync_conn)

            table = await conn.run_sync(load_table)
            self._tables[table_name] = table
            return table

    async def execute_query(self, query: Any) -> Optional[List[Dict[str, Any]]]:
        async with self.engine.begin() as conn:
            result = await conn.execute(query)
            rows = [dict(row._mapping) for row in result]
        return rows or None
    
    async def execute_query_select(self, query: Any) -> Optional[List[Dict[str, Any]]]:
        async with self.engine.connect() as conn:
            result = await conn.execute(query)
            rows = [dict(row._mapping) for row in result]
        return rows or None

    """CRUD"""

    @error_handler
    async def fetch_all(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        table = await self.get_table(table_name)
        query = select(table)

        return await self.execute_query_select(query)

    @error_handler
    async def insert(self, table_name: str, data: dict) -> Optional[Dict[str, Any]]:
        table = await self.get_table(table_name)
        query = insert(table).values(data).returning(table)

        rows = await self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    async def find_by(
        self, table_name: str, column: str, value: Any
    ) -> Optional[List[Dict[str, Any]]]:
        table = await self.get_table(table_name)
        query = select(table).where(table.c[column] == value)

        return await self.execute_query_select(query)

    @error_handler
    async def find_join_record(
        self,
        table_name: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        table = await self.get_table(table_name)
        query = select(table).where(
            and_(
                table.c[first_column] == first_value,
                table.c[second_column] == second_value,
            )
        )

        rows = await self.execute_query_select(query)
        return rows[0] if rows else None

    @error_handler
    async def find_ilike(
        self, table_name: str, column: str, value: str
    ) -> Optional[List[Dict[str, Any]]]:
        table = await self.get_table(table_name)
        query = select(table).where(table.c[column].ilike(f"%{value}%"))

        return await self.execute_query_select(query)

    @error_handler
    async def delete_by(
        self, table_name: str, column: str, value: Any
    ) -> Optional[Dict[str, Any]]:
        table = await self.get_table(table_name)
        query = delete(table).where(table.c[column] == value).returning(table)

        rows = await self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    async def delete_join_record(
        self,
        table_name: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        table = await self.get_table(table_name)
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

        rows = await self.execute_query(query)
        return rows[0] if rows else None

    @error_handler
    async def update_by(
        self, table_name: str, column: str, value: Any, updates: dict
    ) -> Optional[Dict[str, Any]]:
        table = await self.get_table(table_name)
        query = (
            update(table)
            .where(table.c[column] == value)
            .values(updates)
            .returning(table)
        )

        rows = await self.execute_query(query)
        return rows[0] if rows else None


supabase_connection = SupabaseConnection()
