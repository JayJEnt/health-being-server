from supabase import create_client, Client

from typing import Any, Dict, Optional
from functools import wraps

from api.handlers.http_exceptions import ResourceNotFound, InternalServerError
from config import settings
from logger import logger


class SupabaseConnection:
    def __init__(self):
        self._url = settings.SUPABASE_URL
        self._key = settings.SUPABASE_KEY
        try:
            self._client: Client = create_client(self._url, self._key)
        except Exception as ex:
            logger.error(f"Supabase connection error: {ex}")
            raise ConnectionRefusedError

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

    @error_handler
    def fetch_all(self, table: str) -> Optional[list[Dict[str, Any]]]:
        response = self._client.table(table).select("*").execute()
        if not response.data:
            return None
        return response.data

    @error_handler
    def insert(self, table: str, data: dict) -> Optional[Dict[str, Any]]:
        response = self._client.table(table).insert(data).execute()
        if not response.data:
            return None
        return response.data[0]

    # owilms start 06-10-2025: Create an insert for multiple rows of data
    @error_handler
    def bulk_insert(self, table: str, data: list[dict]) -> Optional[Dict[str, Any]]:
        response = self._client.table(table).insert(data).execute()
        if not response.data:
            return None
        return response.data

    # owilms end

    @error_handler
    def find_by(
        self, table: str, column: str, value: Any
    ) -> Optional[list[Dict[str, Any]]]:
        response = self._client.table(table).select("*").eq(column, value).execute()
        if not response.data:
            return None
        return response.data

    @error_handler
    def find_join_record(
        self,
        table: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        response = (
            self._client.table(table)
            .select("*")
            .eq(first_column, first_value)
            .eq(second_column, second_value)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]

    @error_handler
    def find_ilike(
        self, table: str, column: str, value: Any
    ) -> Optional[list[Dict[str, Any]]]:
        response = (
            self._client.table(table).select("*").ilike(column, f"%{value}%").execute()
        )
        if not response.data:
            return None
        return response.data

    @error_handler
    def delete_by(
        self, table: str, column: str, value: Any
    ) -> Optional[Dict[str, Any]]:
        response = self._client.table(table).delete().eq(column, value).execute()
        if not response.data:
            return None
        return response.data[0]

    @error_handler
    def delete_join_record(
        self,
        table: str,
        first_column: str,
        first_value: Any,
        second_column: str,
        second_value: Any,
    ) -> Optional[Dict[str, Any]]:
        response = (
            self._client.table(table)
            .delete()
            .eq(first_column, first_value)
            .eq(second_column, second_value)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]

    @error_handler
    def update_by(
        self, table: str, column: str, value: Any, updates: dict
    ) -> Optional[Dict[str, Any]]:
        response = self._client.table(table).update(updates).eq(column, value).execute()
        if not response.data:
            return None
        return response.data[0]


supabase_connection = SupabaseConnection()
